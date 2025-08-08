import asyncio
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Set
from dotenv import load_dotenv
from logger_config import setup_logging
from ai_providers import create_ai_provider
from rate_limiter import RateLimiter, RateLimitConfig
import uuid
from datetime import datetime

logger = logging.getLogger('java_analysis.step2_enhanced_test')

class EnhancedRequirementsProcessorTest:
    def __init__(self):
        load_dotenv()
        self.processed_files: Set[str] = set()
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        self.requirements_dir = Path(self.output_dir) / "requirements_enhanced_test"
        self.requirements_dir.mkdir(parents=True, exist_ok=True)
        
        # Enhanced metadata files
        self.enhanced_metadata_file = Path(self.output_dir) / "enhanced_metadata.json"
        self.architecture_report_file = Path(self.output_dir) / "enhanced_architecture_report.json"
        
        # Test mode settings - very conservative
        rate_config = RateLimitConfig(
            requests_per_minute=10,
            requests_per_hour=500,
            delay_between_requests=8.0,
            exponential_backoff_base=2.0,
            max_retries=3
        )
        self.rate_limiter = RateLimiter(rate_config)
        
        # Test batch processing settings - smaller batches
        self.max_files_per_batch = 2  # Reduced for testing
        self.max_files_to_process = 20  # Limit for testing
        
        # Initialize AI provider
        self.ai_provider = create_ai_provider()
        logger.info(f"TEST MODE: Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")
        
        # Load enhanced metadata
        self.enhanced_metadata = self.load_enhanced_metadata()
        self.architecture_report = self.load_architecture_report()

    def load_enhanced_metadata(self) -> Dict[str, Any]:
        """Load enhanced metadata from Step1_Enhanced"""
        try:
            if not self.enhanced_metadata_file.exists():
                logger.warning(f"Enhanced metadata file not found: {self.enhanced_metadata_file}")
                return {}
            
            with open(self.enhanced_metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            logger.info(f"TEST MODE: Loaded enhanced metadata with {len(metadata)} entries")
            return metadata
            
        except Exception as e:
            logger.error(f"Error loading enhanced metadata: {e}")
            return {}

    def load_architecture_report(self) -> Dict[str, Any]:
        """Load architecture report from Step1_Enhanced"""
        try:
            if not self.architecture_report_file.exists():
                logger.warning(f"Architecture report file not found: {self.architecture_report_file}")
                return {}
            
            with open(self.architecture_report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            logger.info(f"TEST MODE: Loaded architecture report with {len(report.get('layers', {}))} layers")
            return report
            
        except Exception as e:
            logger.error(f"Error loading architecture report: {e}")
            return {}

    def get_layer_directory(self, layer: str) -> Path:
        """Get directory for a specific architectural layer"""
        layer_dir = self.requirements_dir / layer.lower().replace(' ', '_')
        layer_dir.mkdir(parents=True, exist_ok=True)
        return layer_dir

    def get_component_directory(self, layer: str, component: str) -> Path:
        """Get directory for a specific component within a layer"""
        layer_dir = self.get_layer_directory(layer)
        component_dir = layer_dir / component.lower().replace(' ', '_')
        component_dir.mkdir(parents=True, exist_ok=True)
        return component_dir

    def get_unique_filename(self, base_dir: Path, filename: str, extension: str = '.md') -> Path:
        """Get unique filename with numbering if file exists"""
        base_name = filename
        counter = 0
        
        while True:
            if counter == 0:
                full_filename = f"{base_name}{extension}"
            else:
                full_filename = f"{base_name}-{counter}{extension}"
            
            file_path = base_dir / full_filename
            if not file_path.exists():
                return file_path
            
            counter += 1

    def prioritize_enhanced_files_test(self, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize files for testing - select only high-priority files"""
        prioritized_files = []
        
        # Group files by layer and component
        layer_groups = {}
        for file_path, file_data in metadata.items():
            if not isinstance(file_data, dict):
                continue
                
            classification = file_data.get('classification', {})
            layer = classification.get('primary_layer', 'Unknown')
            component = classification.get('component', 'Unknown')
            
            if layer not in layer_groups:
                layer_groups[layer] = {}
            if component not in layer_groups[layer]:
                layer_groups[layer][component] = []
            
            layer_groups[layer][component].append({
                'file_path': file_path,
                'file_data': file_data,
                'layer': layer,
                'component': component,
                'classification': classification
            })
        
        # Priority order for layers - focus on most important for testing
        layer_priority = [
            'Presentation Layer',
            'Business Logic Layer'
        ]
        
        # Process only priority layers in test mode
        for layer in layer_priority:
            if layer in layer_groups:
                for component, files in layer_groups[layer].items():
                    # Sort files within component by complexity score and take only top ones
                    files.sort(key=lambda x: x['classification'].get('complexity_score', 0), reverse=True)
                    prioritized_files.extend(files[:2])  # Only take top 2 files per component
                    
                    # Limit total files to process
                    if len(prioritized_files) >= self.max_files_to_process:
                        break
                        
            if len(prioritized_files) >= self.max_files_to_process:
                break
        
        logger.info(f"TEST MODE: Selected {len(prioritized_files)} files for testing")
        return prioritized_files

    async def analyze_enhanced_files_batch_test(self, files_batch: List[Dict[str, Any]]) -> None:
        """Test version of analyze_enhanced_files_batch with smaller content"""
        if not files_batch:
            return
            
        logger.info(f"TEST MODE: Analyzing enhanced batch of {len(files_batch)} files")
        
        # Wait for rate limiter before making API call
        await self.rate_limiter.wait_if_needed()
        
        # Create simplified prompt for testing
        files_content = []
        for file_info in files_batch:
            file_path = file_info['file_path']
            file_data = file_info['file_data']
            layer = file_info['layer']
            component = file_info['component']
            classification = file_info['classification']
            
            # Get smaller content preview for testing
            content_preview = file_data.get('content', '')[:300]  # Reduced from 600
            
            # Create simplified file description
            file_description = f"""
File: {file_path}
Layer: {layer}
Component: {component}
Content Preview: {content_preview}
---"""
            files_content.append(file_description)
        
        combined_content = "\n".join(files_content)
        
        # Simplified prompt for testing
        prompt = f"""Analyze the following files and provide enhanced requirements documentation:

{combined_content}

For each file, provide:
1. Architectural Purpose
2. Layer-Specific Functionality
3. Business Requirements
4. Data Flow

Keep responses concise for testing purposes.

Format your response as:
## File: [filename]
### Layer: [layer] | Component: [component]
[analysis]

## File: [filename]
### Layer: [layer] | Component: [component]
[analysis]
..."""
        
        for attempt in range(self.rate_limiter.config.max_retries):
            try:
                # Wait for rate limiter (includes exponential backoff for retries)
                if attempt > 0:
                    await self.rate_limiter.wait_if_needed()
                
                analysis = await self.ai_provider.create_chat_completion(
                    messages=[
                        {"role": "system", "content": "You are a software architect. Provide concise analysis for testing purposes."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1500  # Reduced for testing
                )
                
                # Record successful request
                self.rate_limiter.record_request()
                
                # Parse the response and create organized files
                await self.parse_enhanced_batch_response_test(analysis, files_batch)
                
                # Mark files as processed
                for file_info in files_batch:
                    self.processed_files.add(file_info['file_path'])
                
                logger.info(f"TEST MODE: Successfully analyzed enhanced batch of {len(files_batch)} files")
                
                # Log rate limiting stats
                stats = self.rate_limiter.get_stats()
                logger.info(f"TEST MODE: Rate limit stats: {stats['requests_last_minute']}/min, {stats['requests_last_hour']}/hour")
                
                break
                
            except Exception as e:
                logger.error(f"TEST MODE: Error analyzing enhanced batch (attempt {attempt + 1}): {str(e)}")
                self.rate_limiter.record_failure()
                
                if attempt == self.rate_limiter.config.max_retries - 1:
                    logger.error(f"TEST MODE: Failed to analyze enhanced batch after {self.rate_limiter.config.max_retries} attempts")
                    # Mark files as processed to avoid infinite retries
                    for file_info in files_batch:
                        self.processed_files.add(file_info['file_path'])

    async def parse_enhanced_batch_response_test(self, analysis: str, files_batch: List[Dict[str, Any]]) -> None:
        """Test version of parse_enhanced_batch_response"""
        import re
        
        # Split by file sections
        sections = re.split(r'## File:\s*', analysis)
        
        for i, file_info in enumerate(files_batch):
            file_path = file_info['file_path']
            layer = file_info['layer']
            component = file_info['component']
            classification = file_info['classification']
            
            # Get component directory
            component_dir = self.get_component_directory(layer, component)
            
            # Get unique filename
            base_filename = Path(file_path).stem
            md_file_path = self.get_unique_filename(component_dir, base_filename, '.md')
            
            # Get the corresponding section content
            if i + 1 < len(sections):
                section_content = sections[i + 1].strip()
            else:
                section_content = "TEST MODE: Enhanced analysis not available for this file."
            
            # Create test markdown content with metadata
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            markdown_content = f"""# TEST MODE: Enhanced Requirements Analysis: {file_path}

**Generated**: {timestamp}  
**Mode**: TEST  
**Layer**: {layer}  
**Component**: {component}  
**Classification**: {classification.get('primary_layer', 'Unknown')}  

## Test Analysis

{section_content}

## Test Metadata

```json
{json.dumps(classification, indent=2)}
```
"""
            
            # Write test markdown file
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.debug(f"TEST MODE: Generated enhanced requirements document: {md_file_path}")

    async def process_enhanced_files_with_batching_test(self) -> None:
        """Test version of process_enhanced_files_with_batching"""
        if not self.enhanced_metadata:
            logger.error("TEST MODE: No enhanced metadata available. Please run Step1_Enhanced.sh first.")
            return
        
        prioritized_files = self.prioritize_enhanced_files_test(self.enhanced_metadata)
        
        logger.info(f"TEST MODE: Processing {len(prioritized_files)} enhanced files in batches of {self.max_files_per_batch}")
        
        # Process files in batches
        for i in range(0, len(prioritized_files), self.max_files_per_batch):
            batch = prioritized_files[i:i + self.max_files_per_batch]
            await self.analyze_enhanced_files_batch_test(batch)
            
            # Progress update
            processed_count = len(self.processed_files)
            total_count = len(prioritized_files)
            logger.info(f"TEST MODE: Enhanced progress: {processed_count}/{total_count} files processed")

    def generate_enhanced_index_test(self) -> None:
        """Generate test version of enhanced index"""
        index_path = self.requirements_dir / "step2_enhanced_test_index.md"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# TEST MODE: Enhanced Requirements Documentation Index\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode**: TEST\n")
            f.write(f"**Total files processed**: {len(self.processed_files)}\n\n")
            
            f.write("## TEST: Enhanced Requirements Documents by Layer and Component\n\n")
            
            # Group files by layer and component
            layer_structure = {}
            for file_path in sorted(self.processed_files):
                # Find file in enhanced metadata
                file_data = self.enhanced_metadata.get(file_path, {})
                classification = file_data.get('classification', {})
                layer = classification.get('primary_layer', 'Unknown')
                component = classification.get('component', 'Unknown')
                
                if layer not in layer_structure:
                    layer_structure[layer] = {}
                if component not in layer_structure[layer]:
                    layer_structure[layer][component] = []
                
                layer_structure[layer][component].append(file_path)
            
            # Write organized index
            for layer in sorted(layer_structure.keys()):
                f.write(f"### {layer}\n\n")
                for component in sorted(layer_structure[layer].keys()):
                    f.write(f"#### {component}\n\n")
                    for file_path in layer_structure[layer][component]:
                        md_filename = f"{Path(file_path).stem}.md"
                        relative_path = f"{layer.lower().replace(' ', '_')}/{component.lower().replace(' ', '_')}/{md_filename}"
                        f.write(f"- [{file_path}](./{relative_path})\n")
                    f.write("\n")
        
        logger.info(f"TEST MODE: Generated enhanced index file: {index_path}")

async def generate_enhanced_requirements_test():
    """Test version of main function"""
    logger = setup_logging(level=logging.INFO)
    logger.info("TEST MODE: Starting enhanced requirements generation process")
    
    try:
        processor = EnhancedRequirementsProcessorTest()
        
        # Process enhanced files with batching
        await processor.process_enhanced_files_with_batching_test()
        
        # Generate enhanced index
        processor.generate_enhanced_index_test()
        
        logger.info("TEST MODE: Enhanced requirements generation completed successfully!")
        
    except Exception as e:
        logger.error(f"TEST MODE: Error during enhanced requirements generation: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(generate_enhanced_requirements_test())