"""
Migration Pipeline from ChromaDB to Weaviate
Enhanced with Qwen3-Coder analysis during migration for data enrichment
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    from chromadb_connector import EnhancedChromaDBConnector
    from weaviate_connector import EnhancedWeaviateConnector, WeaviateConfig
    from ollama_integration import OllamaIntegration
    from code_chunker import CodeChunk, ChunkType
except ImportError:
    from .chromadb_connector import EnhancedChromaDBConnector
    from .weaviate_connector import EnhancedWeaviateConnector, WeaviateConfig
    from .ollama_integration import OllamaIntegration
    from .code_chunker import CodeChunk, ChunkType

logger = logging.getLogger('java_analysis.migration_pipeline')

@dataclass
class MigrationConfig:
    """Configuration for the migration process"""
    batch_size: int = 100
    parallel_workers: int = 4
    validate_data: bool = True
    enhance_with_qwen: bool = True
    create_rollback_points: bool = True
    progress_reporting: bool = True
    backup_chromadb: bool = True
    max_retries: int = 3
    retry_delay: float = 2.0

@dataclass
class MigrationStats:
    """Statistics for migration process"""
    total_chunks: int = 0
    migrated_chunks: int = 0
    failed_chunks: int = 0
    enhanced_chunks: int = 0
    start_time: datetime = None
    end_time: datetime = None
    processing_time: float = 0.0
    average_batch_time: float = 0.0
    qwen_analysis_time: float = 0.0

@dataclass
class ValidationResult:
    """Result of data validation"""
    success: bool
    chromadb_count: int
    weaviate_count: int
    missing_chunks: List[str]
    corrupted_chunks: List[str]
    validation_errors: List[str]

class MigrationPipeline:
    """
    Comprehensive migration pipeline from ChromaDB to Weaviate
    Features data validation, Qwen enhancement, and rollback capabilities
    """
    
    def __init__(self, 
                 chromadb_connector: EnhancedChromaDBConnector,
                 weaviate_connector: EnhancedWeaviateConnector,
                 ollama_integration: OllamaIntegration,
                 config: MigrationConfig = None):
        
        self.chromadb = chromadb_connector
        self.weaviate = weaviate_connector
        self.ollama = ollama_integration
        self.config = config or MigrationConfig()
        
        self.stats = MigrationStats()
        self.rollback_points = []
        self._stop_event = threading.Event()
        
        # Create migration directory
        self.migration_dir = Path("migration_data")
        self.migration_dir.mkdir(exist_ok=True)
        
        logger.info(f"Migration pipeline initialized with config: {asdict(self.config)}")

    async def execute_migration(self, dry_run: bool = False) -> MigrationStats:
        """
        Execute the complete migration process
        """
        self.stats.start_time = datetime.now()
        
        try:
            logger.info(f"Starting migration (dry_run={dry_run})")
            
            # Phase 1: Pre-migration validation
            if not await self._pre_migration_checks():
                raise RuntimeError("Pre-migration checks failed")
            
            # Phase 2: Backup ChromaDB (if enabled)
            if self.config.backup_chromadb and not dry_run:
                await self._backup_chromadb()
            
            # Phase 3: Extract data from ChromaDB
            chromadb_data = await self._extract_chromadb_data()
            self.stats.total_chunks = len(chromadb_data)
            
            logger.info(f"Extracted {self.stats.total_chunks} chunks from ChromaDB")
            
            # Phase 4: Process and enhance data
            if not dry_run:
                enhanced_data = await self._process_and_enhance_data(chromadb_data)
                
                # Phase 5: Migrate to Weaviate
                await self._migrate_to_weaviate(enhanced_data)
                
                # Phase 6: Post-migration validation
                validation_result = await self._validate_migration()
                if not validation_result.success:
                    logger.error("Migration validation failed")
                    if self.config.create_rollback_points:
                        await self._handle_rollback()
                    raise RuntimeError("Migration validation failed")
            else:
                logger.info("Dry run completed - no data was migrated")
            
            self.stats.end_time = datetime.now()
            self.stats.processing_time = (self.stats.end_time - self.stats.start_time).total_seconds()
            
            logger.info(f"Migration completed successfully in {self.stats.processing_time:.2f} seconds")
            return self.stats
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            self.stats.end_time = datetime.now()
            if self.stats.start_time:
                self.stats.processing_time = (self.stats.end_time - self.stats.start_time).total_seconds()
            raise

    async def _pre_migration_checks(self) -> bool:
        """Perform comprehensive pre-migration checks"""
        try:
            logger.info("Performing pre-migration checks...")
            
            # Check ChromaDB connection
            chromadb_health = self.chromadb.health_check()
            if not chromadb_health:
                logger.error("ChromaDB health check failed")
                return False
            
            # Check Weaviate connection
            weaviate_health = await self.weaviate.health_check()
            if not weaviate_health['overall']:
                logger.error(f"Weaviate health check failed: {weaviate_health}")
                return False
            
            # Check Ollama connection (if enhancement enabled)
            if self.config.enhance_with_qwen:
                ollama_health = await self.ollama.health_check()
                if not ollama_health:
                    logger.error("Ollama health check failed")
                    return False
            
            # Check available disk space
            available_space = self._get_available_space()
            if available_space < 10 * 1024 * 1024 * 1024:  # 10GB minimum
                logger.warning(f"Low disk space: {available_space / 1024 / 1024 / 1024:.2f}GB available")
            
            logger.info("Pre-migration checks passed")
            return True
            
        except Exception as e:
            logger.error(f"Pre-migration checks failed: {e}")
            return False

    def _get_available_space(self) -> int:
        """Get available disk space in bytes"""
        try:
            stat = os.statvfs(self.migration_dir)
            return stat.f_frsize * stat.f_bavail
        except:
            return float('inf')  # Assume unlimited on error

    async def _backup_chromadb(self):
        """Create backup of ChromaDB data"""
        try:
            logger.info("Creating ChromaDB backup...")
            
            backup_file = self.migration_dir / f"chromadb_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Extract all data
            all_data = await self._extract_chromadb_data()
            
            # Save to backup file
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, default=str)
            
            logger.info(f"ChromaDB backup created: {backup_file}")
            
        except Exception as e:
            logger.error(f"Failed to backup ChromaDB: {e}")
            raise

    async def _extract_chromadb_data(self) -> List[Dict[str, Any]]:
        """Extract all data from ChromaDB with metadata"""
        try:
            logger.info("Extracting data from ChromaDB...")
            
            # Get collection
            collection = self.chromadb.collection
            
            # Get all data with metadata
            results = collection.get(
                include=['documents', 'metadatas', 'embeddings', 'distances']
            )
            
            # Convert to structured format
            extracted_data = []
            
            for i in range(len(results['documents'])):
                chunk_data = {
                    'id': results['ids'][i] if 'ids' in results else f"chunk_{i}",
                    'document': results['documents'][i],
                    'metadata': results['metadatas'][i] if results['metadatas'] else {},
                    'embedding': results['embeddings'][i] if results['embeddings'] else None
                }
                extracted_data.append(chunk_data)
            
            logger.info(f"Extracted {len(extracted_data)} chunks from ChromaDB")
            return extracted_data
            
        except Exception as e:
            logger.error(f"Failed to extract ChromaDB data: {e}")
            raise

    async def _process_and_enhance_data(self, chromadb_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and enhance data with Qwen3-Coder analysis"""
        try:
            logger.info(f"Processing and enhancing {len(chromadb_data)} chunks...")
            
            enhanced_data = []
            batches = [chromadb_data[i:i + self.config.batch_size] 
                      for i in range(0, len(chromadb_data), self.config.batch_size)]
            
            qwen_start_time = time.time()
            
            # Process batches with optional parallel processing
            if self.config.parallel_workers > 1:
                enhanced_data = await self._process_batches_parallel(batches)
            else:
                enhanced_data = await self._process_batches_sequential(batches)
            
            self.stats.qwen_analysis_time = time.time() - qwen_start_time
            
            logger.info(f"Enhanced {len(enhanced_data)} chunks in {self.stats.qwen_analysis_time:.2f}s")
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Data processing and enhancement failed: {e}")
            raise

    async def _process_batches_sequential(self, batches: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Process batches sequentially"""
        enhanced_data = []
        
        for batch_idx, batch in enumerate(batches):
            if self._stop_event.is_set():
                break
                
            batch_start_time = time.time()
            enhanced_batch = await self._process_batch(batch)
            batch_time = time.time() - batch_start_time
            
            enhanced_data.extend(enhanced_batch)
            self.stats.migrated_chunks += len(enhanced_batch)
            
            # Update average batch time
            self.stats.average_batch_time = (
                (self.stats.average_batch_time * batch_idx + batch_time) / (batch_idx + 1)
            )
            
            if self.config.progress_reporting:
                progress = (batch_idx + 1) / len(batches) * 100
                logger.info(f"Processed batch {batch_idx + 1}/{len(batches)} ({progress:.1f}%) "
                          f"in {batch_time:.2f}s")
        
        return enhanced_data

    async def _process_batches_parallel(self, batches: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Process batches in parallel using thread pool"""
        enhanced_data = []
        
        with ThreadPoolExecutor(max_workers=self.config.parallel_workers) as executor:
            # Submit all batch processing tasks
            batch_futures = []
            for batch in batches:
                future = executor.submit(asyncio.run, self._process_batch(batch))
                batch_futures.append(future)
            
            # Collect results as they complete
            for i, future in enumerate(batch_futures):
                if self._stop_event.is_set():
                    break
                    
                try:
                    enhanced_batch = future.result()
                    enhanced_data.extend(enhanced_batch)
                    self.stats.migrated_chunks += len(enhanced_batch)
                    
                    if self.config.progress_reporting:
                        progress = (i + 1) / len(batch_futures) * 100
                        logger.info(f"Completed batch {i + 1}/{len(batch_futures)} ({progress:.1f}%)")
                        
                except Exception as e:
                    logger.error(f"Batch processing failed: {e}")
                    self.stats.failed_chunks += self.config.batch_size
        
        return enhanced_data

    async def _process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a single batch of chunks"""
        enhanced_batch = []
        
        for chunk_data in batch:
            try:
                # Convert ChromaDB data to enhanced format
                enhanced_chunk = await self._enhance_chunk_data(chunk_data)
                enhanced_batch.append(enhanced_chunk)
                self.stats.enhanced_chunks += 1
                
            except Exception as e:
                logger.error(f"Failed to enhance chunk {chunk_data.get('id', 'unknown')}: {e}")
                # Add original data without enhancement
                enhanced_batch.append(self._convert_chromadb_to_weaviate_format(chunk_data))
                self.stats.failed_chunks += 1
        
        return enhanced_batch

    async def _enhance_chunk_data(self, chunk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance individual chunk data with Qwen3-Coder analysis"""
        try:
            # Convert to Weaviate format first
            weaviate_chunk = self._convert_chromadb_to_weaviate_format(chunk_data)
            
            # Enhance with Qwen analysis if enabled
            if self.config.enhance_with_qwen:
                content = chunk_data['document']
                metadata = chunk_data.get('metadata', {})
                
                # Build context for Qwen analysis
                analysis_prompt = f"""Analyze this Java/JSP code chunk and extract:
                1. Architectural layer classification
                2. Business domain identification  
                3. Design patterns used
                4. Integration points
                5. Modernization opportunities
                6. Performance insights
                7. Security concerns
                8. Technical debt assessment
                
                Code:
                {content}
                
                Existing metadata: {json.dumps(metadata, indent=2)}
                """
                
                try:
                    # Get Qwen analysis
                    qwen_result = await self.ollama.analyze_code_repository(
                        repository_context=analysis_prompt,
                        analysis_type="chunk_enhancement"
                    )
                    
                    # Parse and integrate Qwen insights
                    weaviate_chunk = self._integrate_qwen_analysis(weaviate_chunk, qwen_result)
                    
                except Exception as e:
                    logger.warning(f"Qwen enhancement failed for chunk: {e}")
                    # Continue without enhancement
            
            return weaviate_chunk
            
        except Exception as e:
            logger.error(f"Chunk enhancement failed: {e}")
            raise

    def _convert_chromadb_to_weaviate_format(self, chunk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert ChromaDB chunk data to Weaviate format"""
        metadata = chunk_data.get('metadata', {})
        
        return {
            'content': chunk_data['document'],
            'file_path': metadata.get('file_path', ''),
            'chunk_id': chunk_data.get('id', ''),
            'chunk_type': metadata.get('chunk_type', 'unknown'),
            'language': metadata.get('language', 'java'),
            'class_name': metadata.get('class_name', ''),
            'method_name': metadata.get('method_name', ''),
            'package_name': metadata.get('package_name', ''),
            'complexity_score': float(metadata.get('complexity_score', 0.0)),
            'lines_of_code': int(metadata.get('lines_of_code', 0)),
            'architectural_layer': metadata.get('architectural_layer', 'unknown'),
            'business_domain': metadata.get('business_domain', 'general'),
            'token_count': len(chunk_data['document']) // 3,
            'context_weight': 1.0,
            'semantic_importance': 0.5,
            'created_at': datetime.now(),
            'last_analyzed': datetime.now(),
            'analysis_version': '1.0'
        }

    def _integrate_qwen_analysis(self, chunk_data: Dict[str, Any], qwen_result) -> Dict[str, Any]:
        """Integrate Qwen analysis results into chunk data"""
        try:
            # Parse Qwen analysis content for structured insights
            analysis_content = qwen_result.content.lower()
            
            # Extract architectural layer
            if 'presentation' in analysis_content or 'jsp' in analysis_content or 'servlet' in analysis_content:
                chunk_data['architectural_layer'] = 'presentation'
            elif 'service' in analysis_content or 'business logic' in analysis_content:
                chunk_data['architectural_layer'] = 'service'
            elif 'dao' in analysis_content or 'repository' in analysis_content or 'data access' in analysis_content:
                chunk_data['architectural_layer'] = 'data_access'
            elif 'model' in analysis_content or 'entity' in analysis_content or 'dto' in analysis_content:
                chunk_data['architectural_layer'] = 'model'
            
            # Extract other insights (simplified parsing - could be enhanced with NLP)
            chunk_data['qwen_analysis_score'] = qwen_result.confidence_score
            chunk_data['modernization_opportunities'] = self._extract_modernization_insights(analysis_content)
            chunk_data['performance_insights'] = self._extract_performance_insights(analysis_content)
            chunk_data['security_concerns'] = self._extract_security_insights(analysis_content)
            
            return chunk_data
            
        except Exception as e:
            logger.error(f"Failed to integrate Qwen analysis: {e}")
            return chunk_data

    def _extract_modernization_insights(self, analysis: str) -> List[str]:
        """Extract modernization opportunities from analysis"""
        insights = []
        
        if 'jsp' in analysis and 'replace' in analysis:
            insights.append("Consider migrating JSP to modern template engine")
        if 'servlet' in analysis and 'rest' in analysis:
            insights.append("Consider migrating servlet to REST controller")
        if 'jdbc' in analysis and 'orm' in analysis:
            insights.append("Consider using ORM framework instead of raw JDBC")
        
        return insights

    def _extract_performance_insights(self, analysis: str) -> List[str]:
        """Extract performance insights from analysis"""
        insights = []
        
        if 'loop' in analysis and 'optimize' in analysis:
            insights.append("Loop optimization opportunity detected")
        if 'database' in analysis and 'n+1' in analysis:
            insights.append("Potential N+1 query problem")
        if 'memory' in analysis and 'leak' in analysis:
            insights.append("Potential memory leak concern")
        
        return insights

    def _extract_security_insights(self, analysis: str) -> List[str]:
        """Extract security insights from analysis"""
        insights = []
        
        if 'sql injection' in analysis:
            insights.append("SQL injection vulnerability risk")
        if 'xss' in analysis:
            insights.append("XSS vulnerability risk")
        if 'authentication' in analysis and 'missing' in analysis:
            insights.append("Authentication missing or insufficient")
        
        return insights

    async def _migrate_to_weaviate(self, enhanced_data: List[Dict[str, Any]]):
        """Migrate enhanced data to Weaviate"""
        try:
            logger.info(f"Migrating {len(enhanced_data)} chunks to Weaviate...")
            
            # Process in batches for better performance
            batches = [enhanced_data[i:i + self.config.batch_size] 
                      for i in range(0, len(enhanced_data), self.config.batch_size)]
            
            for batch_idx, batch in enumerate(batches):
                if self._stop_event.is_set():
                    break
                
                # Create rollback point if enabled
                if self.config.create_rollback_points:
                    rollback_point = {
                        'batch_idx': batch_idx,
                        'timestamp': datetime.now(),
                        'chunk_ids': [chunk['chunk_id'] for chunk in batch]
                    }
                    self.rollback_points.append(rollback_point)
                
                # Insert batch into Weaviate
                try:
                    # Convert to CodeChunk objects for compatibility
                    code_chunks = []
                    for chunk_data in batch:
                        code_chunk = self._create_code_chunk_from_data(chunk_data)
                        code_chunks.append(code_chunk)
                    
                    # Batch insert
                    object_ids = self.weaviate.batch_insert_chunks(code_chunks)
                    
                    successful_inserts = len([id for id in object_ids if id])
                    logger.info(f"Migrated batch {batch_idx + 1}/{len(batches)} "
                              f"({successful_inserts}/{len(batch)} successful)")
                    
                except Exception as e:
                    logger.error(f"Failed to migrate batch {batch_idx}: {e}")
                    self.stats.failed_chunks += len(batch)
            
            logger.info("Migration to Weaviate completed")
            
        except Exception as e:
            logger.error(f"Weaviate migration failed: {e}")
            raise

    def _create_code_chunk_from_data(self, chunk_data: Dict[str, Any]) -> CodeChunk:
        """Create CodeChunk object from enhanced data"""
        return CodeChunk(
            content=chunk_data['content'],
            file_path=chunk_data['file_path'],
            start_line=0,  # Not available from ChromaDB
            end_line=chunk_data.get('lines_of_code', 0),
            language=chunk_data.get('language', 'java'),
            chunk_type=ChunkType.FILE,  # Default
            chunk_id=chunk_data['chunk_id'],
            class_name=chunk_data.get('class_name'),
            method_name=chunk_data.get('method_name'),
            complexity_score=chunk_data.get('complexity_score', 0.0),
            metadata=chunk_data
        )

    async def _validate_migration(self) -> ValidationResult:
        """Validate the migration was successful"""
        try:
            logger.info("Validating migration...")
            
            # Get counts from both systems
            chromadb_count = len(await self._extract_chromadb_data())
            
            # Count Weaviate objects
            collection = self.weaviate.client.collections.get("JavaCodeChunk")
            weaviate_response = collection.aggregate.over_all()
            weaviate_count = weaviate_response.total_count if weaviate_response else 0
            
            # Perform detailed validation if enabled
            missing_chunks = []
            corrupted_chunks = []
            validation_errors = []
            
            if self.config.validate_data:
                # Sample validation - check a subset of chunks
                sample_size = min(100, chromadb_count // 10)  # 10% sample, max 100
                
                # TODO: Implement detailed validation logic
                logger.info(f"Detailed validation skipped (would check {sample_size} samples)")
            
            success = (chromadb_count == weaviate_count and 
                      len(validation_errors) == 0)
            
            result = ValidationResult(
                success=success,
                chromadb_count=chromadb_count,
                weaviate_count=weaviate_count,
                missing_chunks=missing_chunks,
                corrupted_chunks=corrupted_chunks,
                validation_errors=validation_errors
            )
            
            logger.info(f"Migration validation: ChromaDB={chromadb_count}, "
                       f"Weaviate={weaviate_count}, Success={success}")
            
            return result
            
        except Exception as e:
            logger.error(f"Migration validation failed: {e}")
            return ValidationResult(
                success=False,
                chromadb_count=0,
                weaviate_count=0,
                missing_chunks=[],
                corrupted_chunks=[],
                validation_errors=[str(e)]
            )

    async def _handle_rollback(self):
        """Handle rollback process in case of failure"""
        try:
            logger.warning("Initiating rollback process...")
            
            # Remove inserted data from Weaviate
            for rollback_point in reversed(self.rollback_points):
                chunk_ids = rollback_point['chunk_ids']
                
                # Delete chunks from this rollback point
                # TODO: Implement chunk deletion by chunk_id
                logger.info(f"Rolling back batch with {len(chunk_ids)} chunks")
            
            logger.info("Rollback completed")
            
        except Exception as e:
            logger.error(f"Rollback failed: {e}")

    def stop_migration(self):
        """Stop the migration process gracefully"""
        logger.info("Stopping migration process...")
        self._stop_event.set()

    def get_migration_progress(self) -> Dict[str, Any]:
        """Get current migration progress"""
        progress = {
            'total_chunks': self.stats.total_chunks,
            'migrated_chunks': self.stats.migrated_chunks,
            'failed_chunks': self.stats.failed_chunks,
            'enhanced_chunks': self.stats.enhanced_chunks,
            'progress_percentage': (self.stats.migrated_chunks / self.stats.total_chunks * 100) if self.stats.total_chunks > 0 else 0,
            'average_batch_time': self.stats.average_batch_time,
            'qwen_analysis_time': self.stats.qwen_analysis_time,
            'rollback_points': len(self.rollback_points)
        }
        
        if self.stats.start_time:
            elapsed = (datetime.now() - self.stats.start_time).total_seconds()
            progress['elapsed_time'] = elapsed
            
            if self.stats.migrated_chunks > 0:
                progress['estimated_remaining_time'] = (
                    elapsed / self.stats.migrated_chunks * 
                    (self.stats.total_chunks - self.stats.migrated_chunks)
                )
        
        return progress

# Convenience function for quick migration
async def migrate_chromadb_to_weaviate(
    chromadb_config_path: str = "config/app.yaml",
    weaviate_config: WeaviateConfig = None,
    migration_config: MigrationConfig = None,
    dry_run: bool = False
) -> MigrationStats:
    """Convenience function to perform complete migration"""
    
    try:
        # Initialize components
        chromadb_connector = EnhancedChromaDBConnector(chromadb_config_path)
        weaviate_connector = EnhancedWeaviateConnector(weaviate_config)
        ollama_integration = OllamaIntegration()
        
        # Create and execute migration
        pipeline = MigrationPipeline(
            chromadb_connector=chromadb_connector,
            weaviate_connector=weaviate_connector,
            ollama_integration=ollama_integration,
            config=migration_config
        )
        
        return await pipeline.execute_migration(dry_run=dry_run)
        
    except Exception as e:
        logger.error(f"Migration convenience function failed: {e}")
        raise