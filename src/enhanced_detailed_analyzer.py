#!/usr/bin/env python3
"""
Enhanced Detailed Java Analyzer
Provides comprehensive analysis of Java applications with deep data structure insights
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

@dataclass
class FieldDetail:
    name: str
    type: str
    access_modifier: str
    annotations: List[str]
    is_static: bool
    is_final: bool
    is_collection: bool
    is_relationship: bool
    collection_type: Optional[str]
    generic_types: List[str]
    default_value: Optional[str]
    javadoc: Optional[str]
    validation_rules: List[str]

@dataclass
class MethodDetail:
    name: str
    return_type: str
    access_modifier: str
    parameters: List[Dict[str, Any]]
    annotations: List[str]
    is_static: bool
    is_abstract: bool
    is_final: bool
    throws_exceptions: List[str]
    javadoc: Optional[str]
    complexity_score: int

@dataclass
class DetailedDataStructure:
    name: str
    type: str
    file_path: str
    package_name: str
    access_modifier: str
    fields: List[FieldDetail]
    methods: List[MethodDetail]
    constructors: List[MethodDetail]
    inner_classes: List[str]
    annotations: List[str]
    implements_interfaces: List[str]
    extends_class: Optional[str]
    imports: List[str]
    business_domain: str
    architectural_layer: str
    design_patterns: List[str]
    complexity_score: int
    relationships: List[Dict[str, Any]]
    javadoc: Optional[str]
    file_size_bytes: int
    lines_of_code: int
    created_date: Optional[str]
    last_modified: Optional[str]

class EnhancedDetailedAnalyzer:
    def __init__(self, java_root_path: str, output_dir: str = "./output"):
        self.java_root_path = Path(java_root_path)
        self.output_dir = Path(output_dir)
        
        # Enhanced pattern recognition
        self.patterns = {
            # Basic Java patterns
            'package': re.compile(r'^\s*package\s+([\w\.]+)\s*;', re.MULTILINE),
            'import': re.compile(r'^\s*import\s+(?:static\s+)?([\w\.\*]+)\s*;', re.MULTILINE),
            'class': re.compile(r'^\s*(?:/\*\*.*?\*/\s*)?(?:@\w+(?:\([^)]*\))?\s*)*\s*(public|private|protected)?\s*(abstract|final)?\s*class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w\s,]+))?\s*\{', re.MULTILINE | re.DOTALL),
            'interface': re.compile(r'^\s*(?:/\*\*.*?\*/\s*)?(?:@\w+(?:\([^)]*\))?\s*)*\s*(public|private|protected)?\s*interface\s+(\w+)(?:\s+extends\s+([\w\s,]+))?\s*\{', re.MULTILINE | re.DOTALL),
            'enum': re.compile(r'^\s*(?:/\*\*.*?\*/\s*)?(?:@\w+(?:\([^)]*\))?\s*)*\s*(public|private|protected)?\s*enum\s+(\w+)(?:\s+implements\s+([\w\s,]+))?\s*\{', re.MULTILINE | re.DOTALL),
            'field': re.compile(r'^\s*(?:/\*\*.*?\*/\s*)?(?:@\w+(?:\([^)]*\))?\s*)*\s*(public|private|protected)?\s*(static)?\s*(final)?\s*(transient|volatile)?\s*([\w\<\>\[\]]+)\s+(\w+)(?:\s*=\s*([^;]+))?;', re.MULTILINE),
            'method': re.compile(r'^\s*(?:/\*\*.*?\*/\s*)?(?:@\w+(?:\([^)]*\))?\s*)*\s*(public|private|protected)?\s*(static)?\s*(final|abstract)?\s*(synchronized)?\s*([\w\<\>\[\]]+)\s+(\w+)\s*\(([^)]*)\)(?:\s+throws\s+([\w\s,]+))?\s*(?:\{|;)', re.MULTILINE),
            'constructor': re.compile(r'^\s*(?:/\*\*.*?\*/\s*)?(?:@\w+(?:\([^)]*\))?\s*)*\s*(public|private|protected)?\s*(\w+)\s*\(([^)]*)\)(?:\s+throws\s+([\w\s,]+))?\s*\{', re.MULTILINE),
            'annotation': re.compile(r'@(\w+)(?:\(([^)]*)\))?', re.MULTILINE),
            'javadoc': re.compile(r'/\*\*(.*?)\*/', re.DOTALL),
            'inner_class': re.compile(r'\s+(?:public|private|protected)?\s*(?:static)?\s*class\s+(\w+)', re.MULTILINE),
            
            # JPA/Hibernate patterns
            'jpa_entity': re.compile(r'@Entity(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            'jpa_table': re.compile(r'@Table\(([^)]*)\)', re.MULTILINE | re.IGNORECASE),
            'jpa_id': re.compile(r'@Id', re.MULTILINE | re.IGNORECASE),
            'jpa_generated_value': re.compile(r'@GeneratedValue(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            'jpa_column': re.compile(r'@Column\(([^)]*)\)', re.MULTILINE | re.IGNORECASE),
            'jpa_one_to_one': re.compile(r'@OneToOne(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            'jpa_one_to_many': re.compile(r'@OneToMany(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            'jpa_many_to_one': re.compile(r'@ManyToOne(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            'jpa_many_to_many': re.compile(r'@ManyToMany(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            'jpa_join_column': re.compile(r'@JoinColumn(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            'jpa_join_table': re.compile(r'@JoinTable(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            
            # Spring patterns
            'spring_service': re.compile(r'@Service(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            'spring_repository': re.compile(r'@Repository(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            'spring_controller': re.compile(r'@(?:Controller|RestController)(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            'spring_component': re.compile(r'@Component(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            'spring_autowired': re.compile(r'@Autowired', re.MULTILINE | re.IGNORECASE),
            'spring_qualifier': re.compile(r'@Qualifier\(([^)]*)\)', re.MULTILINE | re.IGNORECASE),
            'spring_request_mapping': re.compile(r'@(?:RequestMapping|GetMapping|PostMapping|PutMapping|DeleteMapping)(?:\([^)]*\))?', re.MULTILINE | re.IGNORECASE),
            
            # Validation patterns
            'validation_not_null': re.compile(r'@NotNull', re.MULTILINE | re.IGNORECASE),
            'validation_not_empty': re.compile(r'@NotEmpty', re.MULTILINE | re.IGNORECASE),
            'validation_size': re.compile(r'@Size\(([^)]*)\)', re.MULTILINE | re.IGNORECASE),
            'validation_min': re.compile(r'@Min\(([^)]*)\)', re.MULTILINE | re.IGNORECASE),
            'validation_max': re.compile(r'@Max\(([^)]*)\)', re.MULTILINE | re.IGNORECASE),
            'validation_pattern': re.compile(r'@Pattern\(([^)]*)\)', re.MULTILINE | re.IGNORECASE),
            'validation_email': re.compile(r'@Email', re.MULTILINE | re.IGNORECASE),
            
            # Lombok patterns
            'lombok_data': re.compile(r'@Data', re.MULTILINE | re.IGNORECASE),
            'lombok_getter': re.compile(r'@Getter', re.MULTILINE | re.IGNORECASE),
            'lombok_setter': re.compile(r'@Setter', re.MULTILINE | re.IGNORECASE),
            'lombok_builder': re.compile(r'@Builder', re.MULTILINE | re.IGNORECASE),
            'lombok_no_args_constructor': re.compile(r'@NoArgsConstructor', re.MULTILINE | re.IGNORECASE),
            'lombok_all_args_constructor': re.compile(r'@AllArgsConstructor', re.MULTILINE | re.IGNORECASE),
        }
        
        # Business domain keywords
        self.business_domains = {
            'customer': ['customer', 'client', 'account', 'user', 'person', 'contact', 'kunde', 'client'],
            'product': ['product', 'service', 'tariff', 'plan', 'package', 'offering', 'produkt', 'dienst'],
            'billing': ['billing', 'invoice', 'payment', 'charge', 'fee', 'cost', 'price', 'rechnung'],
            'order': ['order', 'purchase', 'transaction', 'sale', 'contract', 'bestellung', 'auftrag'],
            'support': ['ticket', 'issue', 'case', 'support', 'help', 'problem', 'incident'],
            'network': ['network', 'device', 'equipment', 'infrastructure', 'netzwerk'],
            'security': ['security', 'auth', 'permission', 'role', 'access', 'login', 'token'],
            'admin': ['admin', 'configuration', 'setting', 'parameter', 'management', 'config']
        }
        
        # Architectural layers
        self.architectural_layers = {
            'presentation': ['controller', 'servlet', 'web', 'ui', 'view', 'jsp', 'gwt'],
            'service': ['service', 'business', 'logic', 'facade'],
            'repository': ['repository', 'dao', 'data', 'persistence'],
            'domain': ['entity', 'model', 'domain', 'aggregate'],
            'dto': ['dto', 'transfer', 'request', 'response', 'form'],
            'config': ['config', 'configuration', 'setup', 'properties'],
            'util': ['util', 'helper', 'common', 'shared', 'tool']
        }
        
        # Design patterns
        self.design_patterns = {
            'singleton': ['singleton', 'instance'],
            'factory': ['factory', 'creator', 'builder'],
            'observer': ['observer', 'listener', 'event'],
            'strategy': ['strategy', 'policy'],
            'decorator': ['decorator', 'wrapper'],
            'adapter': ['adapter', 'bridge'],
            'proxy': ['proxy', 'delegate'],
            'mvc': ['controller', 'model', 'view'],
            'repository': ['repository', 'dao'],
            'service': ['service', 'facade']
        }
        
        self.discovered_structures: List[DetailedDataStructure] = []
        
    async def run_detailed_analysis(self) -> Dict[str, Any]:
        """Run comprehensive detailed analysis"""
        start_time = time.time()
        
        logger.info("🚀 Starting Enhanced Detailed Java Application Analysis")
        logger.info("="*80)
        logger.info(f"📁 Java source directory: {self.java_root_path}")
        logger.info(f"📤 Output directory: {self.output_dir}")
        logger.info(f"🔍 Analysis mode: DEEP STRUCTURE DISCOVERY")
        
        # Phase 1: Discover all Java files
        logger.info("\n📂 Phase 1: Comprehensive Java File Discovery")
        logger.info("-" * 50)
        java_files = await self._discover_all_java_files()
        
        # Phase 2: Detailed analysis of each file
        logger.info("\n🏗️ Phase 2: Deep Structure Analysis")
        logger.info("-" * 50)
        await self._analyze_all_structures_detailed(java_files)
        
        # Phase 3: Relationship analysis
        logger.info("\n🔗 Phase 3: Relationship and Dependency Analysis")
        logger.info("-" * 50)
        relationships = await self._analyze_detailed_relationships()
        
        # Phase 4: Architecture analysis
        logger.info("\n🏛️ Phase 4: Architectural Pattern Analysis")
        logger.info("-" * 50)
        architecture_insights = await self._analyze_architecture_patterns()
        
        # Phase 5: Generate comprehensive reports
        logger.info("\n📊 Phase 5: Comprehensive Report Generation")
        logger.info("-" * 50)
        reports = await self._generate_detailed_reports()
        
        processing_time = time.time() - start_time
        
        # Final results
        results = {
            'timestamp': datetime.now().isoformat(),
            'processing_time': processing_time,
            'files_analyzed': len(java_files),
            'structures_discovered': len(self.discovered_structures),
            'relationships_found': len(relationships),
            'architecture_insights': architecture_insights,
            'comprehensive_analysis': True,
            'success': True
        }
        
        await self._save_detailed_results(results, reports, relationships)
        
        logger.info("\n" + "="*80)
        logger.info("🎉 ENHANCED DETAILED ANALYSIS COMPLETED")
        logger.info("="*80)
        logger.info(f"⏱️  Total Processing Time: {processing_time:.2f} seconds")
        logger.info(f"📁 Files Analyzed: {len(java_files)}")
        logger.info(f"🏗️  Structures Discovered: {len(self.discovered_structures)}")
        logger.info(f"🔗 Relationships Found: {len(relationships)}")
        logger.info(f"📊 Analysis Depth: COMPREHENSIVE")
        
        # Display detailed summary
        await self._display_detailed_summary()
        
        return results
        
    async def _discover_all_java_files(self) -> List[Dict[str, Any]]:
        """Discover all Java files with detailed metadata"""
        java_files = []
        
        if not self.java_root_path.exists():
            logger.error(f"❌ Java source directory does not exist: {self.java_root_path}")
            return []
            
        logger.info(f"🔍 Scanning Java applications in: {self.java_root_path}")
        
        file_count = 0
        processed_files = 0
        skipped_files = 0
        error_files = 0
        
        # Collect module statistics
        module_stats = defaultdict(int)
        
        for file_path in self.java_root_path.rglob("*.java"):
            file_count += 1
            
            if file_count % 100 == 0:
                logger.info(f"   📄 Scanning progress: {file_count} files, {processed_files} processed")
            
            if file_path.is_file():
                file_size = file_path.stat().st_size
                if file_size < 10_000_000:  # Skip very large files (10MB+)
                    try:
                        file_info = await self._analyze_file_metadata(file_path)
                        if file_info:
                            java_files.append(file_info)
                            processed_files += 1
                            
                            # Track module statistics
                            module_name = self._determine_module_name(file_path)
                            module_stats[module_name] += 1
                        else:
                            skipped_files += 1
                    except Exception as e:
                        error_files += 1
                        logger.warning(f"❌ Could not analyze {file_path}: {e}")
                else:
                    skipped_files += 1
                    logger.warning(f"⚠️  Skipping large file ({file_size/1024/1024:.1f}MB): {file_path}")
        
        logger.info("📊 Java File Discovery Results:")
        logger.info(f"   📁 Total Java files found: {file_count}")
        logger.info(f"   ✅ Successfully processed: {processed_files}")
        logger.info(f"   ⏭️  Skipped files: {skipped_files}")
        logger.info(f"   ❌ Error files: {error_files}")
        
        logger.info("🏢 Module Distribution:")
        for module, count in sorted(module_stats.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"   📦 {module}: {count} files")
        
        return java_files
        
    async def _analyze_file_metadata(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze file with basic metadata"""
        try:
            stat_info = file_path.stat()
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return {
                'file_path': str(file_path),
                'content': content,
                'size_bytes': len(content),
                'lines_of_code': len(content.splitlines()),
                'created_date': datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                'last_modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                'module_name': self._determine_module_name(file_path)
            }
        except Exception as e:
            logger.warning(f"Failed to analyze file metadata for {file_path}: {e}")
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
        
    async def _analyze_all_structures_detailed(self, java_files: List[Dict[str, Any]]):
        """Analyze all Java structures with detailed information"""
        logger.info(f"🔍 Performing deep structure analysis on {len(java_files)} files...")
        
        analyzed_count = 0
        structure_count = 0
        
        for file_info in java_files:
            try:
                structures = await self._extract_detailed_structures(file_info)
                self.discovered_structures.extend(structures)
                structure_count += len(structures)
                analyzed_count += 1
                
                if analyzed_count % 200 == 0:
                    logger.info(f"   🏗️  Analysis progress: {analyzed_count}/{len(java_files)} files, {structure_count} structures found")
                    
            except Exception as e:
                logger.warning(f"Failed to analyze structures in {file_info.get('file_path', 'unknown')}: {e}")
        
        logger.info(f"✅ Structure Analysis Complete:")
        logger.info(f"   📁 Files analyzed: {analyzed_count}")
        logger.info(f"   🏗️  Structures discovered: {structure_count}")
        
        # Analyze structure types
        structure_types = defaultdict(int)
        for structure in self.discovered_structures:
            structure_types[structure.type] += 1
            
        logger.info("📊 Structure Type Distribution:")
        for struct_type, count in sorted(structure_types.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"   {struct_type.title()}: {count}")
            
    async def _extract_detailed_structures(self, file_info: Dict[str, Any]) -> List[DetailedDataStructure]:
        """Extract detailed structure information from a Java file"""
        content = file_info['content']
        file_path = file_info['file_path']
        structures = []
        
        # Extract package information
        package_match = self.patterns['package'].search(content)
        package_name = package_match.group(1) if package_match else 'default'
        
        # Extract imports
        import_matches = self.patterns['import'].findall(content)
        imports = [imp.strip() for imp in import_matches]
        
        # Extract Javadoc comments
        javadoc_matches = self.patterns['javadoc'].findall(content)
        main_javadoc = javadoc_matches[0] if javadoc_matches else None
        
        # Analyze different structure types
        
        # 1. Classes
        class_matches = self.patterns['class'].findall(content)
        for match in class_matches:
            if len(match) >= 3:
                access_modifier = match[0] or 'package'
                modifiers = match[1] or ''
                class_name = match[2]
                extends_class = match[3] if len(match) > 3 else None
                implements = match[4] if len(match) > 4 else None
                
                structure = await self._create_detailed_structure(
                    name=class_name,
                    type='abstract_class' if 'abstract' in modifiers else 'class',
                    content=content,
                    file_info=file_info,
                    package_name=package_name,
                    access_modifier=access_modifier,
                    extends_class=extends_class,
                    implements_interfaces=implements.split(',') if implements else [],
                    imports=imports,
                    javadoc=main_javadoc
                )
                if structure:
                    structures.append(structure)
        
        # 2. Interfaces
        interface_matches = self.patterns['interface'].findall(content)
        for match in interface_matches:
            if len(match) >= 2:
                access_modifier = match[0] or 'package'
                interface_name = match[1]
                extends = match[2] if len(match) > 2 else None
                
                structure = await self._create_detailed_structure(
                    name=interface_name,
                    type='interface',
                    content=content,
                    file_info=file_info,
                    package_name=package_name,
                    access_modifier=access_modifier,
                    extends_class=None,
                    implements_interfaces=extends.split(',') if extends else [],
                    imports=imports,
                    javadoc=main_javadoc
                )
                if structure:
                    structures.append(structure)
        
        # 3. Enums
        enum_matches = self.patterns['enum'].findall(content)
        for match in enum_matches:
            if len(match) >= 2:
                access_modifier = match[0] or 'package'
                enum_name = match[1]
                implements = match[2] if len(match) > 2 else None
                
                structure = await self._create_detailed_structure(
                    name=enum_name,
                    type='enum',
                    content=content,
                    file_info=file_info,
                    package_name=package_name,
                    access_modifier=access_modifier,
                    extends_class=None,
                    implements_interfaces=implements.split(',') if implements else [],
                    imports=imports,
                    javadoc=main_javadoc
                )
                if structure:
                    structures.append(structure)
        
        return structures
        
    async def _create_detailed_structure(self, name: str, type: str, content: str, 
                                       file_info: Dict[str, Any], package_name: str,
                                       access_modifier: str, extends_class: Optional[str],
                                       implements_interfaces: List[str], imports: List[str],
                                       javadoc: Optional[str]) -> Optional[DetailedDataStructure]:
        """Create a detailed data structure object"""
        try:
            # Extract detailed fields
            fields = await self._extract_detailed_fields(content)
            
            # Extract detailed methods
            methods = await self._extract_detailed_methods(content)
            
            # Extract constructors
            constructors = await self._extract_constructors(content, name)
            
            # Extract inner classes
            inner_classes = self.patterns['inner_class'].findall(content)
            
            # Extract annotations
            annotations = self.patterns['annotation'].findall(content)
            annotation_names = [ann[0] for ann in annotations]
            
            # Determine business domain
            business_domain = self._determine_business_domain(package_name, name, content)
            
            # Determine architectural layer
            architectural_layer = self._determine_architectural_layer(package_name, name, content, annotation_names)
            
            # Identify design patterns
            design_patterns = self._identify_design_patterns(name, content, annotation_names)
            
            # Calculate complexity
            complexity_score = self._calculate_detailed_complexity(content, fields, methods)
            
            # Extract relationships
            relationships = await self._extract_structure_relationships(content, fields)
            
            return DetailedDataStructure(
                name=name,
                type=type,
                file_path=file_info['file_path'],
                package_name=package_name,
                access_modifier=access_modifier,
                fields=fields,
                methods=methods,
                constructors=constructors,
                inner_classes=inner_classes,
                annotations=annotation_names,
                implements_interfaces=implements_interfaces,
                extends_class=extends_class,
                imports=imports,
                business_domain=business_domain,
                architectural_layer=architectural_layer,
                design_patterns=design_patterns,
                complexity_score=complexity_score,
                relationships=relationships,
                javadoc=javadoc,
                file_size_bytes=file_info['size_bytes'],
                lines_of_code=file_info['lines_of_code'],
                created_date=file_info.get('created_date'),
                last_modified=file_info.get('last_modified')
            )
            
        except Exception as e:
            logger.warning(f"Failed to create detailed structure for {name}: {e}")
            return None
    
    async def _extract_detailed_fields(self, content: str) -> List[FieldDetail]:
        """Extract detailed field information"""
        fields = []
        field_matches = self.patterns['field'].findall(content)
        
        for match in field_matches:
            try:
                if len(match) >= 6:
                    access_modifier = match[0] or 'package'
                    is_static = bool(match[1])
                    is_final = bool(match[2])
                    field_type = match[4]
                    field_name = match[5]
                    default_value = match[6] if len(match) > 6 else None
                    
                    # Skip constants and obvious non-fields
                    if field_name.isupper() or field_name.startswith('get') or field_name.startswith('set'):
                        continue
                    
                    # Extract field annotations
                    field_annotations = self._extract_field_annotations(content, field_name)
                    
                    # Determine collection type and generic types
                    collection_type, generic_types = self._analyze_field_type(field_type)
                    
                    # Extract validation rules
                    validation_rules = self._extract_validation_rules(field_annotations)
                    
                    # Extract field Javadoc
                    field_javadoc = self._extract_field_javadoc(content, field_name)
                    
                    field_detail = FieldDetail(
                        name=field_name,
                        type=field_type,
                        access_modifier=access_modifier,
                        annotations=field_annotations,
                        is_static=is_static,
                        is_final=is_final,
                        is_collection=self._is_collection_type(field_type),
                        is_relationship=self._is_relationship_field(field_annotations),
                        collection_type=collection_type,
                        generic_types=generic_types,
                        default_value=default_value,
                        javadoc=field_javadoc,
                        validation_rules=validation_rules
                    )
                    
                    fields.append(field_detail)
                    
            except Exception as e:
                logger.debug(f"Failed to parse field: {e}")
                continue
        
        return fields
    
    async def _extract_detailed_methods(self, content: str) -> List[MethodDetail]:
        """Extract detailed method information"""
        methods = []
        method_matches = self.patterns['method'].findall(content)
        
        for match in method_matches:
            try:
                if len(match) >= 6:
                    access_modifier = match[0] or 'package'
                    is_static = bool(match[1])
                    modifiers = match[2] or ''
                    is_abstract = 'abstract' in modifiers
                    is_final = 'final' in modifiers
                    return_type = match[4]
                    method_name = match[5]
                    parameters_str = match[6]
                    throws_str = match[7] if len(match) > 7 else None
                    
                    # Parse parameters
                    parameters = self._parse_method_parameters(parameters_str)
                    
                    # Parse throws exceptions
                    throws_exceptions = throws_str.split(',') if throws_str else []
                    throws_exceptions = [ex.strip() for ex in throws_exceptions]
                    
                    # Extract method annotations
                    method_annotations = self._extract_method_annotations(content, method_name)
                    
                    # Extract method Javadoc
                    method_javadoc = self._extract_method_javadoc(content, method_name)
                    
                    # Calculate method complexity
                    method_complexity = self._calculate_method_complexity(content, method_name)
                    
                    method_detail = MethodDetail(
                        name=method_name,
                        return_type=return_type,
                        access_modifier=access_modifier,
                        parameters=parameters,
                        annotations=method_annotations,
                        is_static=is_static,
                        is_abstract=is_abstract,
                        is_final=is_final,
                        throws_exceptions=throws_exceptions,
                        javadoc=method_javadoc,
                        complexity_score=method_complexity
                    )
                    
                    methods.append(method_detail)
                    
            except Exception as e:
                logger.debug(f"Failed to parse method: {e}")
                continue
        
        return methods
    
    async def _extract_constructors(self, content: str, class_name: str) -> List[MethodDetail]:
        """Extract constructor information"""
        constructors = []
        constructor_matches = self.patterns['constructor'].findall(content)
        
        for match in constructor_matches:
            try:
                if len(match) >= 3 and match[1] == class_name:
                    access_modifier = match[0] or 'package'
                    parameters_str = match[2]
                    throws_str = match[3] if len(match) > 3 else None
                    
                    # Parse parameters
                    parameters = self._parse_method_parameters(parameters_str)
                    
                    # Parse throws exceptions
                    throws_exceptions = throws_str.split(',') if throws_str else []
                    throws_exceptions = [ex.strip() for ex in throws_exceptions]
                    
                    constructor_detail = MethodDetail(
                        name=class_name,
                        return_type=class_name,
                        access_modifier=access_modifier,
                        parameters=parameters,
                        annotations=[],
                        is_static=False,
                        is_abstract=False,
                        is_final=False,
                        throws_exceptions=throws_exceptions,
                        javadoc=None,
                        complexity_score=0
                    )
                    
                    constructors.append(constructor_detail)
                    
            except Exception as e:
                logger.debug(f"Failed to parse constructor: {e}")
                continue
        
        return constructors
    
    def _extract_field_annotations(self, content: str, field_name: str) -> List[str]:
        """Extract annotations for a specific field"""
        annotations = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if field_name in line and any(modifier in line for modifier in ['private ', 'public ', 'protected ']):
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
    
    def _analyze_field_type(self, field_type: str) -> Tuple[Optional[str], List[str]]:
        """Analyze field type for collection type and generics"""
        collection_type = None
        generic_types = []
        
        # Check for collection types
        if '<' in field_type and '>' in field_type:
            base_type = field_type.split('<')[0]
            generic_part = field_type[field_type.index('<')+1:field_type.rindex('>')]
            
            if base_type in ['List', 'Set', 'Collection', 'ArrayList', 'HashSet', 'LinkedList', 'Map', 'HashMap']:
                collection_type = base_type
                generic_types = [g.strip() for g in generic_part.split(',')]
        
        return collection_type, generic_types
    
    def _extract_validation_rules(self, annotations: List[str]) -> List[str]:
        """Extract validation rules from annotations"""
        validation_rules = []
        
        validation_mapping = {
            'NotNull': 'Field cannot be null',
            'NotEmpty': 'Field cannot be empty',
            'NotBlank': 'Field cannot be blank',
            'Size': 'Field size validation',
            'Min': 'Minimum value validation',
            'Max': 'Maximum value validation',
            'Email': 'Email format validation',
            'Pattern': 'Regex pattern validation'
        }
        
        for annotation in annotations:
            if annotation in validation_mapping:
                validation_rules.append(validation_mapping[annotation])
        
        return validation_rules
    
    def _extract_field_javadoc(self, content: str, field_name: str) -> Optional[str]:
        """Extract Javadoc for a specific field"""
        # Simplified Javadoc extraction
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if field_name in line and any(modifier in line for modifier in ['private ', 'public ', 'protected ']):
                # Look for Javadoc comment before field
                j = i - 1
                javadoc_lines = []
                while j >= 0:
                    if '/**' in lines[j]:
                        # Found start of Javadoc, collect until */
                        k = j
                        while k <= i - 1:
                            javadoc_lines.append(lines[k])
                            if '*/' in lines[k]:
                                break
                            k += 1
                        return '\n'.join(javadoc_lines)
                    elif lines[j].strip() == '':
                        j -= 1
                    else:
                        break
                break
        
        return None
    
    def _parse_method_parameters(self, parameters_str: str) -> List[Dict[str, Any]]:
        """Parse method parameters"""
        parameters = []
        
        if not parameters_str or parameters_str.strip() == '':
            return parameters
        
        # Split parameters by comma, but be careful with generics
        param_parts = []
        current_param = ""
        bracket_count = 0
        
        for char in parameters_str:
            if char == '<':
                bracket_count += 1
            elif char == '>':
                bracket_count -= 1
            elif char == ',' and bracket_count == 0:
                param_parts.append(current_param.strip())
                current_param = ""
                continue
            current_param += char
        
        if current_param.strip():
            param_parts.append(current_param.strip())
        
        for param in param_parts:
            param = param.strip()
            if param:
                parts = param.split()
                if len(parts) >= 2:
                    param_type = ' '.join(parts[:-1])
                    param_name = parts[-1]
                    
                    parameters.append({
                        'name': param_name,
                        'type': param_type
                    })
        
        return parameters
    
    def _extract_method_annotations(self, content: str, method_name: str) -> List[str]:
        """Extract annotations for a specific method"""
        annotations = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if method_name in line and '(' in line and any(modifier in line for modifier in ['public ', 'private ', 'protected ']):
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
    
    def _extract_method_javadoc(self, content: str, method_name: str) -> Optional[str]:
        """Extract Javadoc for a specific method"""
        # Similar to field Javadoc extraction
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if method_name in line and '(' in line and any(modifier in line for modifier in ['public ', 'private ', 'protected ']):
                # Look for Javadoc comment before method
                j = i - 1
                javadoc_lines = []
                while j >= 0:
                    if '/**' in lines[j]:
                        # Found start of Javadoc, collect until */
                        k = j
                        while k <= i - 1:
                            javadoc_lines.append(lines[k])
                            if '*/' in lines[k]:
                                break
                            k += 1
                        return '\n'.join(javadoc_lines)
                    elif lines[j].strip() == '':
                        j -= 1
                    else:
                        break
                break
        
        return None
    
    def _calculate_method_complexity(self, content: str, method_name: str) -> int:
        """Calculate complexity score for a specific method"""
        # Find method body and calculate complexity
        lines = content.split('\n')
        method_lines = []
        in_method = False
        brace_count = 0
        
        for line in lines:
            if not in_method and method_name in line and '(' in line:
                in_method = True
                if '{' in line:
                    brace_count += line.count('{')
                    brace_count -= line.count('}')
                continue
            
            if in_method:
                method_lines.append(line)
                brace_count += line.count('{')
                brace_count -= line.count('}')
                
                if brace_count == 0:
                    break
        
        # Calculate complexity based on method content
        method_content = '\n'.join(method_lines)
        complexity = 1  # Base complexity
        complexity += method_content.count('if')
        complexity += method_content.count('for')
        complexity += method_content.count('while')
        complexity += method_content.count('switch')
        complexity += method_content.count('catch')
        complexity += method_content.count('&&')
        complexity += method_content.count('||')
        
        return min(complexity, 50)
    
    def _is_collection_type(self, field_type: str) -> bool:
        """Check if field type is a collection"""
        collection_types = ['List', 'Set', 'Collection', 'ArrayList', 'HashSet', 'LinkedList', 'Map', 'HashMap', 'Queue', 'Deque']
        return any(ctype in field_type for ctype in collection_types)
    
    def _is_relationship_field(self, annotations: List[str]) -> bool:
        """Check if field represents a relationship"""
        relationship_annotations = ['OneToOne', 'OneToMany', 'ManyToOne', 'ManyToMany', 'JoinColumn', 'JoinTable']
        return any(ann in annotations for ann in relationship_annotations)
    
    def _determine_business_domain(self, package_name: str, class_name: str, content: str) -> str:
        """Determine business domain with enhanced logic"""
        domains = []
        text_to_analyze = f"{package_name} {class_name} {content}".lower()
        
        for domain, keywords in self.business_domains.items():
            score = sum(1 for keyword in keywords if keyword in text_to_analyze)
            if score > 0:
                domains.append((domain, score))
        
        # Return domains sorted by relevance score
        domains.sort(key=lambda x: x[1], reverse=True)
        return ', '.join([domain[0] for domain in domains[:3]]) if domains else 'general'
    
    def _determine_architectural_layer(self, package_name: str, class_name: str, content: str, annotations: List[str]) -> str:
        """Determine architectural layer"""
        text_to_analyze = f"{package_name} {class_name} {' '.join(annotations)}".lower()
        
        for layer, keywords in self.architectural_layers.items():
            if any(keyword in text_to_analyze for keyword in keywords):
                return layer
        
        return 'unknown'
    
    def _identify_design_patterns(self, class_name: str, content: str, annotations: List[str]) -> List[str]:
        """Identify design patterns"""
        patterns = []
        text_to_analyze = f"{class_name} {content} {' '.join(annotations)}".lower()
        
        for pattern, keywords in self.design_patterns.items():
            if any(keyword in text_to_analyze for keyword in keywords):
                patterns.append(pattern)
        
        return patterns
    
    def _calculate_detailed_complexity(self, content: str, fields: List[FieldDetail], methods: List[MethodDetail]) -> int:
        """Calculate detailed complexity score"""
        complexity = 0
        
        # Base complexity from content
        complexity += content.count('if')
        complexity += content.count('for')
        complexity += content.count('while')
        complexity += content.count('switch')
        complexity += content.count('catch')
        complexity += content.count('&&')
        complexity += content.count('||')
        
        # Add complexity from fields
        complexity += len(fields) * 0.5
        
        # Add complexity from methods
        for method in methods:
            complexity += method.complexity_score
        
        return min(int(complexity), 100)
    
    async def _extract_structure_relationships(self, content: str, fields: List[FieldDetail]) -> List[Dict[str, Any]]:
        """Extract relationships between structures"""
        relationships = []
        
        for field in fields:
            if field.is_relationship:
                relationship_type = 'unknown'
                
                # Determine relationship type from annotations
                for annotation in field.annotations:
                    if 'OneToOne' in annotation:
                        relationship_type = 'one_to_one'
                    elif 'OneToMany' in annotation:
                        relationship_type = 'one_to_many'
                    elif 'ManyToOne' in annotation:
                        relationship_type = 'many_to_one'
                    elif 'ManyToMany' in annotation:
                        relationship_type = 'many_to_many'
                    break
                
                relationships.append({
                    'field_name': field.name,
                    'target_type': field.type,
                    'relationship_type': relationship_type,
                    'is_collection': field.is_collection,
                    'annotations': field.annotations
                })
        
        return relationships
    
    async def _analyze_detailed_relationships(self) -> List[Dict[str, Any]]:
        """Analyze relationships between all discovered structures"""
        logger.info("🔗 Analyzing detailed relationships...")
        
        relationships = []
        structure_map = {structure.name: structure for structure in self.discovered_structures}
        
        relationship_count = 0
        
        for structure in self.discovered_structures:
            for relationship in structure.relationships:
                target_type = relationship.get('target_type', '')
                
                # Check if target type exists in our structures
                if target_type in structure_map:
                    relationships.append({
                        'source': structure.name,
                        'target': target_type,
                        'source_package': structure.package_name,
                        'target_package': structure_map[target_type].package_name,
                        'relationship_type': relationship.get('relationship_type', 'unknown'),
                        'field_name': relationship.get('field_name', ''),
                        'is_collection': relationship.get('is_collection', False),
                        'annotations': relationship.get('annotations', [])
                    })
                    relationship_count += 1
        
        logger.info(f"✅ Found {relationship_count} detailed relationships")
        return relationships
    
    async def _analyze_architecture_patterns(self) -> Dict[str, Any]:
        """Analyze architectural patterns in the codebase"""
        logger.info("🏛️ Analyzing architectural patterns...")
        
        # Analyze layer distribution
        layer_distribution = defaultdict(int)
        domain_distribution = defaultdict(int)
        pattern_distribution = defaultdict(int)
        
        for structure in self.discovered_structures:
            layer_distribution[structure.architectural_layer] += 1
            
            for domain in structure.business_domain.split(', '):
                if domain != 'general':
                    domain_distribution[domain] += 1
            
            for pattern in structure.design_patterns:
                pattern_distribution[pattern] += 1
        
        # Calculate architecture quality metrics
        total_structures = len(self.discovered_structures)
        average_complexity = sum(s.complexity_score for s in self.discovered_structures) / total_structures if total_structures > 0 else 0
        
        return {
            'layer_distribution': dict(layer_distribution),
            'domain_distribution': dict(domain_distribution),
            'pattern_distribution': dict(pattern_distribution),
            'total_structures': total_structures,
            'average_complexity': average_complexity,
            'high_complexity_structures': [s.name for s in self.discovered_structures if s.complexity_score > 30]
        }
    
    async def _generate_detailed_reports(self) -> Dict[str, Any]:
        """Generate comprehensive detailed reports"""
        logger.info("📊 Generating comprehensive reports...")
        
        # Structure analysis report
        structure_report = {
            'total_structures': len(self.discovered_structures),
            'by_type': defaultdict(list),
            'by_domain': defaultdict(list),
            'by_layer': defaultdict(list),
            'by_module': defaultdict(list)
        }
        
        for structure in self.discovered_structures:
            structure_data = {
                'name': structure.name,
                'package': structure.package_name,
                'fields_count': len(structure.fields),
                'methods_count': len(structure.methods),
                'complexity': structure.complexity_score,
                'file_path': structure.file_path
            }
            
            structure_report['by_type'][structure.type].append(structure_data)
            structure_report['by_domain'][structure.business_domain].append(structure_data)
            structure_report['by_layer'][structure.architectural_layer].append(structure_data)
            
            module_name = self._determine_module_name(Path(structure.file_path))
            structure_report['by_module'][module_name].append(structure_data)
        
        # Convert defaultdicts to regular dicts
        for key in ['by_type', 'by_domain', 'by_layer', 'by_module']:
            structure_report[key] = dict(structure_report[key])
        
        return {
            'structure_analysis': structure_report,
            'field_analysis': await self._analyze_field_patterns(),
            'method_analysis': await self._analyze_method_patterns(),
            'annotation_analysis': await self._analyze_annotation_usage(),
            'complexity_analysis': await self._analyze_complexity_patterns()
        }
    
    async def _analyze_field_patterns(self) -> Dict[str, Any]:
        """Analyze field patterns across all structures"""
        field_types = defaultdict(int)
        annotation_usage = defaultdict(int)
        validation_usage = defaultdict(int)
        collection_usage = defaultdict(int)
        
        for structure in self.discovered_structures:
            for field in structure.fields:
                field_types[field.type] += 1
                
                for annotation in field.annotations:
                    annotation_usage[annotation] += 1
                
                for validation in field.validation_rules:
                    validation_usage[validation] += 1
                
                if field.is_collection and field.collection_type:
                    collection_usage[field.collection_type] += 1
        
        return {
            'common_field_types': dict(Counter(field_types).most_common(20)),
            'annotation_usage': dict(Counter(annotation_usage).most_common(15)),
            'validation_patterns': dict(Counter(validation_usage).most_common(10)),
            'collection_types': dict(Counter(collection_usage).most_common(10))
        }
    
    async def _analyze_method_patterns(self) -> Dict[str, Any]:
        """Analyze method patterns across all structures"""
        method_names = defaultdict(int)
        return_types = defaultdict(int)
        access_modifiers = defaultdict(int)
        
        for structure in self.discovered_structures:
            for method in structure.methods:
                method_names[method.name] += 1
                return_types[method.return_type] += 1
                access_modifiers[method.access_modifier] += 1
        
        return {
            'common_method_names': dict(Counter(method_names).most_common(20)),
            'return_types': dict(Counter(return_types).most_common(15)),
            'access_modifiers': dict(Counter(access_modifiers).most_common(5))
        }
    
    async def _analyze_annotation_usage(self) -> Dict[str, Any]:
        """Analyze annotation usage patterns"""
        class_annotations = defaultdict(int)
        
        for structure in self.discovered_structures:
            for annotation in structure.annotations:
                class_annotations[annotation] += 1
        
        return {
            'class_annotations': dict(Counter(class_annotations).most_common(20))
        }
    
    async def _analyze_complexity_patterns(self) -> Dict[str, Any]:
        """Analyze complexity patterns"""
        complexities = [s.complexity_score for s in self.discovered_structures]
        
        if not complexities:
            return {}
        
        return {
            'average_complexity': sum(complexities) / len(complexities),
            'median_complexity': sorted(complexities)[len(complexities) // 2],
            'max_complexity': max(complexities),
            'min_complexity': min(complexities),
            'complexity_distribution': {
                'low (0-10)': sum(1 for c in complexities if c <= 10),
                'medium (11-25)': sum(1 for c in complexities if 11 <= c <= 25),
                'high (26-50)': sum(1 for c in complexities if 26 <= c <= 50),
                'very_high (51+)': sum(1 for c in complexities if c > 50)
            }
        }
    
    async def _save_detailed_results(self, results: Dict[str, Any], reports: Dict[str, Any], relationships: List[Dict[str, Any]]):
        """Save comprehensive detailed results"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Save main results
        with open(self.output_dir / "detailed_analysis_results.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save detailed structures
        structures_data = {
            'structures': [asdict(structure) for structure in self.discovered_structures],
            'summary': {
                'total_count': len(self.discovered_structures),
                'types': {t: len([s for s in self.discovered_structures if s.type == t]) for t in set(s.type for s in self.discovered_structures)},
                'domains': {d: len([s for s in self.discovered_structures if d in s.business_domain]) for d in set(domain for s in self.discovered_structures for domain in s.business_domain.split(', ') if domain != 'general')},
                'layers': {l: len([s for s in self.discovered_structures if s.architectural_layer == l]) for l in set(s.architectural_layer for s in self.discovered_structures)}
            }
        }
        
        with open(self.output_dir / "detailed_structures_analysis.json", 'w') as f:
            json.dump(structures_data, f, indent=2, default=str)
        
        # Save relationships
        with open(self.output_dir / "detailed_relationships.json", 'w') as f:
            json.dump({'relationships': relationships, 'count': len(relationships)}, f, indent=2, default=str)
        
        # Save comprehensive reports
        with open(self.output_dir / "comprehensive_reports.json", 'w') as f:
            json.dump(reports, f, indent=2, default=str)
        
        logger.info(f"📁 Detailed results saved to {self.output_dir}")
    
    async def _display_detailed_summary(self):
        """Display comprehensive summary of the analysis"""
        logger.info("📈 COMPREHENSIVE ANALYSIS SUMMARY")
        logger.info("-" * 50)
        
        # Structure type summary
        type_counts = defaultdict(int)
        for structure in self.discovered_structures:
            type_counts[structure.type] += 1
        
        logger.info("🏗️ Structure Types Discovered:")
        for struct_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"   {struct_type.title()}: {count}")
        
        # Business domain summary
        domain_counts = defaultdict(int)
        for structure in self.discovered_structures:
            for domain in structure.business_domain.split(', '):
                if domain != 'general':
                    domain_counts[domain] += 1
        
        logger.info("🏢 Business Domain Distribution:")
        for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"   {domain.title()}: {count} structures")
        
        # Architectural layer summary
        layer_counts = defaultdict(int)
        for structure in self.discovered_structures:
            layer_counts[structure.architectural_layer] += 1
        
        logger.info("🏛️ Architectural Layer Distribution:")
        for layer, count in sorted(layer_counts.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"   {layer.title()}: {count} structures")
        
        # Complexity summary
        complexities = [s.complexity_score for s in self.discovered_structures]
        if complexities:
            logger.info("🔧 Complexity Analysis:")
            logger.info(f"   Average Complexity: {sum(complexities) / len(complexities):.1f}")
            logger.info(f"   Maximum Complexity: {max(complexities)}")
            logger.info(f"   High Complexity (>30): {sum(1 for c in complexities if c > 30)} structures")
        
        # Top structures by complexity
        top_complex = sorted(self.discovered_structures, key=lambda x: x.complexity_score, reverse=True)[:5]
        logger.info("🎯 Most Complex Structures:")
        for structure in top_complex:
            logger.info(f"   {structure.name}: {structure.complexity_score} (in {structure.package_name})")

async def main():
    """Main function to run enhanced detailed analysis"""
    java_root_path = "/Users/thomaskamsker/Documents/Atom/vron.one/playground/java"
    analyzer = EnhancedDetailedAnalyzer(java_root_path)
    
    try:
        results = await analyzer.run_detailed_analysis()
        
        if results.get('success', False):
            print('✅ Enhanced detailed Java analysis completed successfully!')
            print(f'📊 Files analyzed: {results.get("files_analyzed", 0)}')
            print(f'🏗️ Structures discovered: {results.get("structures_discovered", 0)}')
            print(f'🔗 Relationships found: {results.get("relationships_found", 0)}')
            print(f'⏱️ Processing time: {results.get("processing_time", 0):.2f} seconds')
            return True
        else:
            print('❌ Enhanced analysis failed')
            return False
            
    except Exception as e:
        print(f'❌ Enhanced analysis failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)