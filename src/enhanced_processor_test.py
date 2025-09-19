#!/usr/bin/env python3
"""
Enhanced Processor Test - Core Java Analysis without Weaviate dependency
Tests the core data structure discovery and analysis functionality
"""

import asyncio
import logging
import json
import os
import time
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Set, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import aiohttp

@dataclass
class DataStructure:
    name: str
    type: str  # 'entity', 'dto', 'enum', 'interface', 'abstract_class'
    file_path: str
    package_name: str
    fields: List[Dict[str, Any]]
    methods: List[str]
    relationships: List[Dict[str, Any]]
    annotations: List[str]
    inheritance: Optional[str]
    complexity_score: int
    business_domain: str

@dataclass
class EntityRelationship:
    source_entity: str
    target_entity: str
    relationship_type: str  # 'one_to_one', 'one_to_many', 'many_to_many', 'composition', 'aggregation'
    field_name: str
    is_bidirectional: bool
    cascade_operations: List[str]

class EnhancedJavaProcessor:
    def __init__(self, java_root_path: str, output_dir: str = "./output", enable_data_structure_discovery: bool = True):
        self.java_root_path = Path(java_root_path)
        self.output_dir = Path(output_dir)
        self.enable_data_structure_discovery = enable_data_structure_discovery
        
        # Data structure storage
        self.discovered_data_structures: List[DataStructure] = []
        self.entity_relationships: List[EntityRelationship] = []
        
        # Enhanced Java patterns for data structure discovery
        self.java_patterns = {
            'package': re.compile(r'^\s*package\s+([\w\.]+)\s*;', re.MULTILINE),
            'class': re.compile(r'^\s*(?:@\w+\s+)*(?:public|private|protected)?\s*(?:abstract|final)?\s*class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w\s,]+))?', re.MULTILINE),
            'interface': re.compile(r'^\s*(?:@\w+\s+)*(?:public|private|protected)?\s*interface\s+(\w+)(?:\s+extends\s+([\w\s,]+))?', re.MULTILINE),
            'enum': re.compile(r'^\s*(?:@\w+\s+)*(?:public|private|protected)?\s*enum\s+(\w+)', re.MULTILINE),
            'field': re.compile(r'^\s*(?:@\w+(?:\([^)]*\))?\s+)*(?:public|private|protected)?\s*(?:static)?\s*(?:final)?\s*([\w\<\>\[\]]+)\s+(\w+)(?:\s*=\s*[^;]+)?;', re.MULTILINE),
            'method': re.compile(r'^\s*(?:@\w+(?:\([^)]*\))?\s+)*(?:public|private|protected)?\s*(?:static)?\s*(?:final)?\s*(?:abstract)?\s*([\w\<\>\[\]]+)\s+(\w+)\s*\([^)]*\)', re.MULTILINE),
            'annotation': re.compile(r'@(\w+)(?:\([^)]*\))?', re.MULTILINE),
            'import': re.compile(r'^\s*import\s+([\w\.\*]+)\s*;', re.MULTILINE),
            
            # JPA/Hibernate patterns
            'entity': re.compile(r'@Entity|@Table', re.MULTILINE | re.IGNORECASE),
            'jpa_id': re.compile(r'@Id|@GeneratedValue', re.MULTILINE | re.IGNORECASE),
            'jpa_column': re.compile(r'@Column', re.MULTILINE | re.IGNORECASE),
            'jpa_relationship': re.compile(r'@(OneToOne|OneToMany|ManyToOne|ManyToMany|JoinColumn|JoinTable)', re.MULTILINE | re.IGNORECASE),
            
            # Spring patterns
            'spring_component': re.compile(r'@(Component|Service|Repository|Controller|RestController)', re.MULTILINE | re.IGNORECASE),
            'spring_autowired': re.compile(r'@Autowired|@Inject|@Resource', re.MULTILINE | re.IGNORECASE),
            
            # DTO patterns
            'dto_annotation': re.compile(r'@Data|@Getter|@Setter|@Builder|@AllArgsConstructor|@NoArgsConstructor', re.MULTILINE | re.IGNORECASE),
            
            # Validation patterns
            'validation': re.compile(r'@(Valid|NotNull|NotEmpty|NotBlank|Size|Min|Max|Email|Pattern)', re.MULTILINE | re.IGNORECASE)
        }
        
        # Business domain keywords
        self.business_domains = {
            'customer': ['customer', 'client', 'account', 'user', 'person', 'contact'],
            'product': ['product', 'service', 'tariff', 'plan', 'package', 'offering'],
            'billing': ['billing', 'invoice', 'payment', 'charge', 'fee', 'cost', 'price'],
            'order': ['order', 'purchase', 'transaction', 'sale', 'contract'],
            'support': ['ticket', 'issue', 'case', 'support', 'help', 'problem'],
            'network': ['network', 'device', 'equipment', 'infrastructure'],
            'security': ['security', 'auth', 'permission', 'role', 'access'],
            'admin': ['admin', 'configuration', 'setting', 'parameter', 'management']
        }

    async def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive analysis with data structure discovery"""
        start_time = time.time()
        
        logger.info("🚀 Starting comprehensive Java analysis with enhanced data structure discovery")
        logger.info(f"📁 Java source directory: {self.java_root_path}")
        logger.info(f"📤 Output directory: {self.output_dir}")
        logger.info(f"🔍 Data structure discovery: {'Enabled' if self.enable_data_structure_discovery else 'Disabled'}")
        
        # Phase 1: Discover and analyze Java files
        logger.info("📂 Phase 1: Discovering Java files...")
        java_files = await self._discover_java_files()
        logger.info(f"✅ Phase 1 completed: {len(java_files)} Java files discovered")
        
        # Phase 2: Extract data structures
        if self.enable_data_structure_discovery:
            logger.info("🏗️ Phase 2: Extracting data structures...")
            await self._extract_data_structures(java_files)
            logger.info(f"✅ Phase 2 completed: {len(self.discovered_data_structures)} data structures extracted")
            
            logger.info("🔗 Phase 3: Analyzing entity relationships...")
            await self._analyze_relationships()
            logger.info(f"✅ Phase 3 completed: {len(self.entity_relationships)} relationships identified")
        else:
            logger.info("⏭️ Skipping data structure discovery (disabled)")
        
        # Phase 3: Generate analysis reports
        logger.info("📊 Phase 4: Generating analysis reports...")
        results = await self._generate_analysis_reports()
        logger.info("✅ Phase 4 completed: Analysis reports generated")
        
        processing_time = time.time() - start_time
        
        # Compile final results
        final_results = {
            'timestamp': datetime.now().isoformat(),
            'processing_time': processing_time,
            'files_processed': len(java_files),
            'data_structures_found': len(self.discovered_data_structures),
            'entity_relationships': len(self.entity_relationships),
            'requirements_generated': results.get('requirements_count', 0),
            'analysis_completed': True,
            'success': True,
            'java_root_path': str(self.java_root_path),
            'output_directory': str(self.output_dir)
        }
        
        # Save final results
        await self._save_results(final_results)
        
        logger.info("="*80)
        logger.info("🎉 COMPREHENSIVE JAVA ANALYSIS COMPLETED SUCCESSFULLY")
        logger.info("="*80)
        logger.info(f"⏱️  Processing Time: {processing_time:.2f} seconds")
        logger.info(f"📁 Files Processed: {len(java_files)}")
        logger.info(f"🏗️  Data Structures Found: {len(self.discovered_data_structures)}")
        logger.info(f"🔗 Entity Relationships: {len(self.entity_relationships)}")
        logger.info(f"📊 Output Files Generated: {self.output_dir}")
        
        # Display summary statistics
        self._display_summary_statistics()
        logger.info("="*80)
        
        return final_results

    async def _discover_java_files(self) -> List[Dict[str, Any]]:
        """Discover and analyze Java files"""
        java_files = []
        
        logger.info(f"🔍 Scanning Java files in: {self.java_root_path}")
        
        # Check if java root path exists
        if not self.java_root_path.exists():
            logger.error(f"❌ Java source directory does not exist: {self.java_root_path}")
            return []
        
        file_count = 0
        skipped_files = 0
        error_files = 0
        
        for file_path in self.java_root_path.rglob("*.java"):
            file_count += 1
            if file_count % 50 == 0:
                logger.info(f"   📄 Scanned {file_count} files, processed {len(java_files)} successfully")
                
            if file_path.is_file():
                file_size = file_path.stat().st_size
                if file_size < 5_000_000:  # Skip very large files (5MB+)
                    try:
                        file_info = await self._analyze_java_file(file_path)
                        if file_info:
                            java_files.append(file_info)
                        else:
                            skipped_files += 1
                    except Exception as e:
                        error_files += 1
                        logger.warning(f"❌ Could not analyze {file_path}: {e}")
                else:
                    skipped_files += 1
                    logger.warning(f"⚠️  Skipping large file ({file_size/1024/1024:.1f}MB): {file_path}")
        
        logger.info("📊 File Discovery Summary:")
        logger.info(f"   📁 Total .java files found: {file_count}")
        logger.info(f"   ✅ Successfully processed: {len(java_files)}")
        logger.info(f"   ⏭️  Skipped files: {skipped_files}")
        logger.info(f"   ❌ Error files: {error_files}")
        
        if len(java_files) == 0:
            logger.warning("⚠️  No Java files could be processed. Check directory path and file accessibility.")
        
        return java_files

    async def _analyze_java_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze individual Java file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract basic information
            package_match = self.java_patterns['package'].search(content)
            package_name = package_match.group(1) if package_match else 'default'
            
            # Extract classes and interfaces
            class_matches = self.java_patterns['class'].findall(content)
            interface_matches = self.java_patterns['interface'].findall(content)
            enum_matches = self.java_patterns['enum'].findall(content)
            
            class_names = [match[0] if isinstance(match, tuple) else match for match in class_matches]
            class_names.extend([match[0] if isinstance(match, tuple) else match for match in interface_matches])
            class_names.extend(enum_matches)
            
            # Extract annotations
            annotation_matches = self.java_patterns['annotation'].findall(content)
            
            # Determine module name
            module_name = self._determine_module_name(file_path)
            
            # Determine business context
            business_context = self._determine_business_context(package_name, class_names, content)
            
            # Calculate complexity
            complexity = self._calculate_complexity(content)
            
            # Determine file type
            file_type = self._determine_file_type(content, class_names, annotation_matches)
            
            return {
                'file_path': str(file_path),
                'package_name': package_name,
                'class_names': class_names,
                'module_name': module_name,
                'business_context': business_context,
                'content': content,
                'complexity': complexity,
                'file_type': file_type,
                'annotations': annotation_matches,
                'size_bytes': len(content),
                'lines_of_code': len(content.splitlines())
            }
            
        except Exception as e:
            logger.warning(f"Failed to analyze {file_path}: {e}")
            return None

    def _determine_module_name(self, file_path: Path) -> str:
        """Determine module name from file path"""
        parts = file_path.parts
        
        for part in parts:
            if any(keyword in part.lower() for keyword in ['cuco', 'administration', 'framework', 'pkb', 'cct']):
                return part
        
        if 'src' in parts:
            src_index = parts.index('src')
            if src_index > 0:
                return parts[src_index - 1]
        
        return 'unknown'

    def _determine_business_context(self, package_name: str, class_names: List[str], content: str) -> str:
        """Determine business context from code analysis"""
        contexts = []
        text_to_analyze = f"{package_name} {' '.join(class_names)} {content}".lower()
        
        for domain, keywords in self.business_domains.items():
            if any(keyword in text_to_analyze for keyword in keywords):
                contexts.append(domain)
        
        return ', '.join(contexts) if contexts else 'general'

    def _calculate_complexity(self, content: str) -> int:
        """Calculate file complexity"""
        complexity = 0
        complexity += content.count('if')
        complexity += content.count('for')
        complexity += content.count('while')
        complexity += content.count('switch')
        complexity += content.count('catch')
        complexity += content.count('&&')
        complexity += content.count('||')
        complexity += len(re.findall(r'^\s*(?:public|private|protected)', content, re.MULTILINE))
        return min(complexity, 100)

    def _determine_file_type(self, content: str, class_names: List[str], annotations: List[str]) -> str:
        """Determine the type of Java file"""
        content_lower = content.lower()
        annotations_lower = [ann.lower() for ann in annotations]
        class_names_lower = [name.lower() for name in class_names]
        
        # Check for entity patterns
        if any(ann in annotations_lower for ann in ['entity', 'table']):
            return 'entity'
        
        # Check for DTO patterns
        if any(ann in annotations_lower for ann in ['data', 'getter', 'setter', 'builder']):
            return 'dto'
        
        # Check for service patterns
        if any(ann in annotations_lower for ann in ['service', 'component']):
            return 'service'
        
        # Check for controller patterns
        if any(ann in annotations_lower for ann in ['controller', 'restcontroller']):
            return 'controller'
        
        # Check for repository patterns
        if any(ann in annotations_lower for ann in ['repository']):
            return 'repository'
        
        # Check by class name patterns
        for class_name in class_names_lower:
            if 'controller' in class_name or 'servlet' in class_name:
                return 'controller'
            elif 'service' in class_name:
                return 'service'
            elif 'repository' in class_name or 'dao' in class_name:
                return 'repository'
            elif 'dto' in class_name or 'data' in class_name:
                return 'dto'
            elif 'entity' in class_name or 'model' in class_name:
                return 'entity'
        
        # Check for interface
        if 'interface ' in content_lower:
            return 'interface'
        
        # Check for enum
        if 'enum ' in content_lower:
            return 'enum'
        
        # Check for abstract class
        if 'abstract class' in content_lower:
            return 'abstract_class'
        
        return 'class'

    async def _extract_data_structures(self, java_files: List[Dict[str, Any]]):
        """Extract data structures from Java files"""
        logger.info("🏗️ Extracting data structures...")
        
        for file_info in java_files:
            content = file_info['content']
            
            # Look for data structure patterns
            if self._is_data_structure(file_info):
                data_structure = await self._analyze_data_structure(file_info)
                if data_structure:
                    self.discovered_data_structures.append(data_structure)
        
        logger.info(f"📊 Found {len(self.discovered_data_structures)} data structures")

    def _is_data_structure(self, file_info: Dict[str, Any]) -> bool:
        """Check if file represents a data structure"""
        file_type = file_info.get('file_type', '').lower()
        annotations = [ann.lower() for ann in file_info.get('annotations', [])]
        
        # Entity types
        data_structure_types = ['entity', 'dto', 'enum', 'interface', 'abstract_class']
        if file_type in data_structure_types:
            return True
        
        # Check for data-related annotations
        data_annotations = ['entity', 'table', 'data', 'getter', 'setter', 'builder']
        if any(ann in annotations for ann in data_annotations):
            return True
        
        return False

    async def _analyze_data_structure(self, file_info: Dict[str, Any]) -> Optional[DataStructure]:
        """Analyze a data structure in detail"""
        try:
            content = file_info['content']
            
            # Extract fields
            fields = self._extract_fields(content)
            
            # Extract methods
            method_matches = self.java_patterns['method'].findall(content)
            methods = [match[1] if isinstance(match, tuple) else match for match in method_matches]
            
            # Extract relationships
            relationships = self._extract_relationships(content)
            
            # Determine inheritance
            inheritance = self._extract_inheritance(content)
            
            # Get primary class name
            class_names = file_info.get('class_names', [])
            primary_name = class_names[0] if class_names else Path(file_info['file_path']).stem
            
            return DataStructure(
                name=primary_name,
                type=file_info.get('file_type', 'class'),
                file_path=file_info['file_path'],
                package_name=file_info.get('package_name', ''),
                fields=fields,
                methods=methods,
                relationships=relationships,
                annotations=file_info.get('annotations', []),
                inheritance=inheritance,
                complexity_score=file_info.get('complexity', 0),
                business_domain=file_info.get('business_context', 'general')
            )
            
        except Exception as e:
            logger.warning(f"Failed to analyze data structure in {file_info.get('file_path', 'unknown')}: {e}")
            return None

    def _extract_fields(self, content: str) -> List[Dict[str, Any]]:
        """Extract field information from Java content"""
        fields = []
        field_matches = self.java_patterns['field'].findall(content)
        
        for match in field_matches:
            if isinstance(match, tuple) and len(match) >= 2:
                field_type, field_name = match[0], match[1]
                
                # Skip static final constants and methods
                if field_name.isupper() or field_name.startswith('get') or field_name.startswith('set'):
                    continue
                
                # Extract annotations for this field
                field_annotations = self._extract_field_annotations(content, field_name)
                
                fields.append({
                    'name': field_name,
                    'type': field_type,
                    'annotations': field_annotations,
                    'is_collection': self._is_collection_type(field_type),
                    'is_relationship': self._is_relationship_field(field_annotations)
                })
        
        return fields

    def _extract_field_annotations(self, content: str, field_name: str) -> List[str]:
        """Extract annotations for a specific field"""
        annotations = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if field_name in line and ('private ' in line or 'public ' in line or 'protected ' in line):
                # Look at previous lines for annotations
                j = i - 1
                while j >= 0 and (lines[j].strip().startswith('@') or lines[j].strip() == ''):
                    if lines[j].strip().startswith('@'):
                        annotation = lines[j].strip()
                        annotation_name = annotation.split('(')[0].replace('@', '')
                        annotations.append(annotation_name)
                    j -= 1
                break
        
        return annotations

    def _is_collection_type(self, field_type: str) -> bool:
        """Check if field type is a collection"""
        collection_types = ['List', 'Set', 'Collection', 'ArrayList', 'HashSet', 'LinkedList']
        return any(ctype in field_type for ctype in collection_types)

    def _is_relationship_field(self, annotations: List[str]) -> bool:
        """Check if field represents a relationship"""
        relationship_annotations = ['OneToOne', 'OneToMany', 'ManyToOne', 'ManyToMany', 'JoinColumn', 'JoinTable']
        return any(ann in annotations for ann in relationship_annotations)

    def _extract_relationships(self, content: str) -> List[Dict[str, Any]]:
        """Extract relationship information"""
        relationships = []
        relationship_matches = self.java_patterns['jpa_relationship'].findall(content)
        
        for match in relationship_matches:
            relationship_type = match.lower()
            relationships.append({
                'type': relationship_type,
                'details': 'Extracted from annotations'
            })
        
        return relationships

    def _extract_inheritance(self, content: str) -> Optional[str]:
        """Extract inheritance information"""
        class_matches = self.java_patterns['class'].findall(content)
        
        for match in class_matches:
            if isinstance(match, tuple) and len(match) > 1 and match[1]:
                return match[1]  # Parent class
        
        return None

    async def _analyze_relationships(self):
        """Analyze relationships between data structures"""
        logger.info("🔗 Analyzing entity relationships...")
        
        # Build entity mapping
        entity_map = {ds.name: ds for ds in self.discovered_data_structures}
        
        for data_structure in self.discovered_data_structures:
            for field in data_structure.fields:
                # Check if field type matches another entity
                if field['type'] in entity_map and field['is_relationship']:
                    relationship = EntityRelationship(
                        source_entity=data_structure.name,
                        target_entity=field['type'],
                        relationship_type=self._determine_relationship_type(field['annotations']),
                        field_name=field['name'],
                        is_bidirectional=False,  # Would need more analysis to determine
                        cascade_operations=[]  # Would need annotation parsing
                    )
                    self.entity_relationships.append(relationship)
        
        logger.info(f"🔗 Found {len(self.entity_relationships)} relationships")

    def _determine_relationship_type(self, annotations: List[str]) -> str:
        """Determine relationship type from annotations"""
        for annotation in annotations:
            if 'OneToOne' in annotation:
                return 'one_to_one'
            elif 'OneToMany' in annotation:
                return 'one_to_many'
            elif 'ManyToOne' in annotation:
                return 'many_to_one'
            elif 'ManyToMany' in annotation:
                return 'many_to_many'
        return 'unknown'

    async def _generate_analysis_reports(self) -> Dict[str, Any]:
        """Generate comprehensive analysis reports"""
        logger.info("📊 Generating analysis reports...")
        
        # Generate data structure analysis
        data_structure_analysis = {
            'entities': [asdict(ds) for ds in self.discovered_data_structures if ds.type == 'entity'],
            'dtos': [asdict(ds) for ds in self.discovered_data_structures if ds.type == 'dto'],
            'enums': [asdict(ds) for ds in self.discovered_data_structures if ds.type == 'enum'],
            'interfaces': [asdict(ds) for ds in self.discovered_data_structures if ds.type == 'interface'],
            'relationships': [asdict(rel) for rel in self.entity_relationships],
            'business_domains': self._analyze_business_domains(),
            'complexity_analysis': self._analyze_complexity()
        }
        
        # Generate module analysis
        module_analysis = self._analyze_modules()
        
        # Generate architecture report
        architecture_report = {
            'modules': module_analysis,
            'data_layer': self._analyze_data_layer(),
            'service_layer': self._analyze_service_layer(),
            'web_layer': self._analyze_web_layer(),
            'integration_points': self._analyze_integration_points()
        }
        
        return {
            'data_structure_analysis': data_structure_analysis,
            'module_analysis': module_analysis,
            'architecture_report': architecture_report,
            'requirements_count': 0,  # Will be filled by requirements generator
            'analysis_objects': len(self.discovered_data_structures) + len(self.entity_relationships)
        }

    def _analyze_business_domains(self) -> Dict[str, Any]:
        """Analyze business domains from data structures"""
        domain_stats = defaultdict(int)
        domain_entities = defaultdict(list)
        
        for ds in self.discovered_data_structures:
            domains = ds.business_domain.split(', ')
            for domain in domains:
                if domain != 'general':
                    domain_stats[domain] += 1
                    domain_entities[domain].append(ds.name)
        
        return {
            'domain_distribution': dict(domain_stats),
            'entities_by_domain': dict(domain_entities)
        }

    def _analyze_complexity(self) -> Dict[str, Any]:
        """Analyze complexity metrics"""
        if not self.discovered_data_structures:
            return {}
        
        complexities = [ds.complexity_score for ds in self.discovered_data_structures]
        
        return {
            'average_complexity': sum(complexities) / len(complexities),
            'max_complexity': max(complexities),
            'min_complexity': min(complexities),
            'high_complexity_structures': [ds.name for ds in self.discovered_data_structures if ds.complexity_score > 20]
        }

    def _analyze_modules(self) -> Dict[str, Any]:
        """Analyze module structure"""
        module_stats = defaultdict(lambda: {'files': 0, 'entities': 0, 'services': 0, 'controllers': 0})
        
        for ds in self.discovered_data_structures:
            module_name = self._determine_module_name(Path(ds.file_path))
            module_stats[module_name]['files'] += 1
            
            if ds.type == 'entity':
                module_stats[module_name]['entities'] += 1
            elif ds.type == 'service':
                module_stats[module_name]['services'] += 1
            elif ds.type == 'controller':
                module_stats[module_name]['controllers'] += 1
        
        return dict(module_stats)

    def _analyze_data_layer(self) -> Dict[str, Any]:
        """Analyze data layer components"""
        entities = [ds for ds in self.discovered_data_structures if ds.type == 'entity']
        repositories = [ds for ds in self.discovered_data_structures if ds.type == 'repository']
        
        return {
            'entity_count': len(entities),
            'repository_count': len(repositories),
            'relationship_count': len(self.entity_relationships),
            'main_entities': [e.name for e in entities[:10]]
        }

    def _analyze_service_layer(self) -> Dict[str, Any]:
        """Analyze service layer components"""
        services = [ds for ds in self.discovered_data_structures if ds.type == 'service']
        
        return {
            'service_count': len(services),
            'main_services': [s.name for s in services[:10]]
        }

    def _analyze_web_layer(self) -> Dict[str, Any]:
        """Analyze web layer components"""
        controllers = [ds for ds in self.discovered_data_structures if ds.type == 'controller']
        
        return {
            'controller_count': len(controllers),
            'main_controllers': [c.name for c in controllers[:10]]
        }

    def _analyze_integration_points(self) -> List[Dict[str, Any]]:
        """Analyze integration points"""
        # This would analyze REST endpoints, external service calls, etc.
        # Simplified for now
        return []

    def _display_summary_statistics(self):
        """Display comprehensive summary statistics"""
        logger.info("📈 ANALYSIS SUMMARY STATISTICS:")
        
        # File type distribution
        file_types = defaultdict(int)
        for ds in self.discovered_data_structures:
            file_types[ds.type] += 1
        
        logger.info("📊 Data Structure Types:")
        for file_type, count in sorted(file_types.items()):
            logger.info(f"   {file_type.title()}: {count}")
        
        # Business domain distribution
        domain_analysis = self._analyze_business_domains()
        domain_dist = domain_analysis.get('domain_distribution', {})
        
        if domain_dist:
            logger.info("🏢 Business Domain Distribution:")
            for domain, count in sorted(domain_dist.items(), key=lambda x: x[1], reverse=True):
                logger.info(f"   {domain.title()}: {count} entities")
        
        # Module distribution
        module_analysis = self._analyze_modules()
        if module_analysis:
            logger.info("📦 Module Distribution:")
            for module, stats in sorted(module_analysis.items()):
                logger.info(f"   {module}: {stats['files']} files, {stats['entities']} entities")
        
        # Complexity analysis
        complexity_analysis = self._analyze_complexity()
        if complexity_analysis:
            logger.info("🔧 Complexity Analysis:")
            logger.info(f"   Average Complexity: {complexity_analysis['average_complexity']:.1f}")
            logger.info(f"   Max Complexity: {complexity_analysis['max_complexity']}")
            high_complexity = complexity_analysis.get('high_complexity_structures', [])
            if high_complexity:
                logger.info(f"   High Complexity Files: {len(high_complexity)}")

    async def _save_results(self, results: Dict[str, Any]):
        """Save analysis results to files"""
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Save main results
            with open(self.output_dir / "test_analysis_metadata.json", 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            # Save data structures analysis
            data_structures_data = {
                'entities': [asdict(ds) for ds in self.discovered_data_structures if ds.type == 'entity'],
                'dtos': [asdict(ds) for ds in self.discovered_data_structures if ds.type == 'dto'],
                'enums': [asdict(ds) for ds in self.discovered_data_structures if ds.type == 'enum'],
                'interfaces': [asdict(ds) for ds in self.discovered_data_structures if ds.type == 'interface'],
                'relationships': [asdict(rel) for rel in self.entity_relationships],
                'summary': {
                    'total_data_structures': len(self.discovered_data_structures),
                    'total_relationships': len(self.entity_relationships),
                    'business_domains': self._analyze_business_domains(),
                    'complexity_metrics': self._analyze_complexity()
                }
            }
            
            with open(self.output_dir / "test_data_structures_analysis.json", 'w') as f:
                json.dump(data_structures_data, f, indent=2, default=str)
            
            # Save architecture report
            architecture_data = {
                'modules': self._analyze_modules(),
                'data_layer': self._analyze_data_layer(),
                'service_layer': self._analyze_service_layer(),
                'web_layer': self._analyze_web_layer(),
                'timestamp': datetime.now().isoformat()
            }
            
            with open(self.output_dir / "test_enhanced_architecture_report.json", 'w') as f:
                json.dump(architecture_data, f, indent=2, default=str)
            
            logger.info(f"📁 Results saved to {self.output_dir}")
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

async def main():
    """Main test function"""
    java_root_path = "/Users/thomaskamsker/Documents/Atom/vron.one/playground/java"
    processor = EnhancedJavaProcessor(java_root_path, enable_data_structure_discovery=True)
    
    try:
        results = await processor.run_comprehensive_analysis()
        
        if results.get('success', False):
            print('✅ Java analysis test completed successfully!')
            print(f'📊 Generated analysis for {results.get("files_processed", 0)} files')
            print(f'🏗️ Discovered {results.get("data_structures_found", 0)} data structures')
            print(f'🔗 Identified {results.get("entity_relationships", 0)} relationships')
            return True
        else:
            print('❌ Java analysis test failed')
            return False
            
    except Exception as e:
        print(f'❌ Java analysis test failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)