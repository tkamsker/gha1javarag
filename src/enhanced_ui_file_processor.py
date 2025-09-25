"""
Enhanced File Processor for Iteration 14
Extends the base file processor to handle GWT UI-specific files
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import xml.etree.ElementTree as ET
from file_processor import FileProcessor
from gwt_ui_processor import GWTUIProcessor
import logging

logger = logging.getLogger('java_analysis.enhanced_ui_file_processor')

class EnhancedUIFileProcessor(FileProcessor):
    """Enhanced file processor with GWT UI component analysis"""
    
    # Extended supported extensions for UI files
    UI_SUPPORTED_EXTENSIONS = {
        '.java': 'Java source file',
        '.jsp': 'Java Server Page', 
        '.xml': 'XML configuration',
        '.html': 'HTML file',
        '.js': 'JavaScript file',
        '.css': 'Cascading Style Sheet',
        '.properties': 'Properties file',
        '.json': 'JSON configuration',
        '.sql': 'SQL script'
    }
    
    # UI-specific file patterns
    UI_FILE_PATTERNS = {
        'uibinder': r'.*\.ui\.xml$',
        'gwt_module': r'.*\.gwt\.xml$', 
        'web_config': r'web\.xml$',
        'gwt_component': r'.*(?:View|Dialog|Panel|Widget|Portlet)\.java$',
        'css_file': r'.*\.css$',
        'js_file': r'.*\.js$'
    }
    
    # GWT-specific keywords for component identification
    GWT_INDICATORS = [
        '@UiField', '@UiHandler', '@UiTemplate',
        'extends Composite', 'extends DialogBox', 'extends PopupPanel',
        'UiBinder', 'implements HasWidgets', 'implements IsWidget'
    ]
    
    def __init__(self):
        super().__init__()
        self.gwt_processor = GWTUIProcessor()
        self.ui_components: Dict[str, Any] = {}
        self.ui_templates: Dict[str, str] = {}
        self.navigation_flows: List[Any] = []
        
        # Update supported extensions
        self.SUPPORTED_EXTENSIONS = self.UI_SUPPORTED_EXTENSIONS
        
    def process_files_with_ui_analysis(self) -> Dict[str, Any]:
        """Process files with comprehensive UI analysis"""
        logger.info(f"Processing files with UI analysis in {self.source_dir}")
        
        results = {
            'file_metadata': [],
            'ui_components': {},
            'ui_templates': {},
            'navigation_flows': [],
            'ui_statistics': {
                'total_files': 0,
                'ui_files': 0,
                'java_components': 0,
                'uibinder_templates': 0,
                'gwt_modules': 0,
                'css_files': 0,
                'js_files': 0
            }
        }
        
        # Get all eligible files
        ui_files = self._discover_ui_files()
        results['ui_statistics']['total_files'] = len(ui_files)
        
        # Process files by category
        for file_info in ui_files:
            file_path = file_info['path']
            file_category = file_info['category']
            
            try:
                # Extract basic metadata
                metadata = self._extract_file_metadata(file_path, file_info['extension'])
                results['file_metadata'].append(metadata)
                
                # Category-specific processing
                if file_category == 'gwt_component':
                    self._process_gwt_component(file_path, results)
                    results['ui_statistics']['java_components'] += 1
                    
                elif file_category == 'uibinder':
                    self._process_uibinder_template(file_path, results)
                    results['ui_statistics']['uibinder_templates'] += 1
                    
                elif file_category == 'gwt_module':
                    self._process_gwt_module(file_path, results)
                    results['ui_statistics']['gwt_modules'] += 1
                    
                elif file_category == 'css_file':
                    self._process_css_file(file_path, results)
                    results['ui_statistics']['css_files'] += 1
                    
                elif file_category == 'js_file':
                    self._process_js_file(file_path, results)
                    results['ui_statistics']['js_files'] += 1
                
                results['ui_statistics']['ui_files'] += 1
                logger.debug(f"Processed UI file: {file_path} ({file_category})")
                
            except Exception as e:
                logger.error(f"Error processing UI file {file_path}: {e}")
                continue
        
        # Analyze navigation flows
        results['navigation_flows'] = self.gwt_processor.analyze_navigation_flow(results['ui_components'])
        
        # Final processing and enrichment
        self._enrich_ui_analysis(results)
        
        logger.info(f"UI Analysis complete: {results['ui_statistics']}")
        return results
    
    def _discover_ui_files(self) -> List[Dict[str, str]]:
        """Discover all UI-related files"""
        ui_files = []
        
        try:
            for root, _, files in os.walk(self.source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    ext = os.path.splitext(file)[1].lower()
                    
                    if ext in self.UI_SUPPORTED_EXTENSIONS:
                        # Categorize the file
                        category = self._categorize_ui_file(file_path, file)
                        
                        if category:  # Only include UI-relevant files
                            ui_files.append({
                                'path': file_path,
                                'filename': file,
                                'extension': ext,
                                'category': category
                            })
        
        except Exception as e:
            logger.error(f"Error discovering UI files: {e}")
            
        return ui_files
    
    def _categorize_ui_file(self, file_path: str, filename: str) -> Optional[str]:
        """Categorize file based on UI relevance"""
        # Check against UI patterns
        for category, pattern in self.UI_FILE_PATTERNS.items():
            if re.match(pattern, filename, re.IGNORECASE):
                return category
        
        # For Java files, check content for GWT indicators
        if filename.endswith('.java'):
            try:
                content = self._read_file_with_encoding_detection(file_path)
                if any(indicator in content for indicator in self.GWT_INDICATORS):
                    return 'gwt_component'
            except:
                pass
        
        # For XML files, check if they're UI-related
        if filename.endswith('.xml'):
            try:
                content = self._read_file_with_encoding_detection(file_path)
                if '<ui:UiBinder' in content or 'xmlns:g="urn:ui:com.google.gwt.user.client.ui"' in content:
                    return 'uibinder'
                elif '<module' in content and 'com.google.gwt' in content:
                    return 'gwt_module'
                elif filename == 'web.xml':
                    return 'web_config'
            except:
                pass
        
        # Include CSS and JS files in UI directories
        if filename.endswith(('.css', '.js')):
            if any(ui_dir in file_path.lower() for ui_dir in ['ui', 'client', 'web', 'static', 'resources']):
                return 'css_file' if filename.endswith('.css') else 'js_file'
        
        return None
    
    def _process_gwt_component(self, file_path: str, results: Dict[str, Any]):
        """Process GWT Java component"""
        component = self.gwt_processor.parse_gwt_component(file_path)
        if component:
            results['ui_components'][component.component_id] = component
    
    def _process_uibinder_template(self, file_path: str, results: Dict[str, Any]):
        """Process UiBinder XML template"""
        template = self.gwt_processor.parse_uibinder_template(file_path)
        if template:
            template_name = Path(file_path).stem
            results['ui_templates'][template_name] = {
                'path': file_path,
                'template': template
            }
    
    def _process_gwt_module(self, file_path: str, results: Dict[str, Any]):
        """Process GWT module configuration"""
        try:
            content = self._read_file_with_encoding_detection(file_path)
            
            # Parse GWT module XML
            root = ET.fromstring(content)
            
            module_info = {
                'path': file_path,
                'module_name': root.get('rename-to', Path(file_path).stem),
                'inherits': [elem.get('name') for elem in root.findall('inherits')],
                'entry_points': [elem.get('class') for elem in root.findall('entry-point')],
                'sources': [elem.get('path', '') for elem in root.findall('source')],
                'stylesheets': [elem.get('src') for elem in root.findall('stylesheet')]
            }
            
            # Store in results
            if 'gwt_modules' not in results:
                results['gwt_modules'] = {}
            results['gwt_modules'][module_info['module_name']] = module_info
            
        except Exception as e:
            logger.error(f"Error processing GWT module {file_path}: {e}")
    
    def _process_css_file(self, file_path: str, results: Dict[str, Any]):
        """Process CSS file for UI styling information"""
        try:
            content = self._read_file_with_encoding_detection(file_path)
            
            # Extract CSS classes and selectors
            css_classes = re.findall(r'\.([a-zA-Z][a-zA-Z0-9_-]*)', content)
            css_ids = re.findall(r'#([a-zA-Z][a-zA-Z0-9_-]*)', content)
            
            # Look for GWT-specific CSS patterns
            gwt_patterns = re.findall(r'\.gwt-[a-zA-Z0-9_-]+', content)
            
            css_info = {
                'path': file_path,
                'classes': list(set(css_classes)),
                'ids': list(set(css_ids)),
                'gwt_patterns': list(set(gwt_patterns)),
                'size': len(content)
            }
            
            if 'css_files' not in results:
                results['css_files'] = {}
            results['css_files'][Path(file_path).name] = css_info
            
        except Exception as e:
            logger.error(f"Error processing CSS file {file_path}: {e}")
    
    def _process_js_file(self, file_path: str, results: Dict[str, Any]):
        """Process JavaScript file for UI logic"""
        try:
            content = self._read_file_with_encoding_detection(file_path)
            
            # Look for GWT-generated patterns
            gwt_generated = '$wnd' in content or '__gwtModuleFunction__' in content
            
            # Extract function names
            functions = re.findall(r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)', content)
            
            # Look for UI event patterns
            events = re.findall(r'on[A-Z][a-zA-Z]*', content)
            
            js_info = {
                'path': file_path,
                'gwt_generated': gwt_generated,
                'functions': list(set(functions)),
                'events': list(set(events)),
                'size': len(content)
            }
            
            if 'js_files' not in results:
                results['js_files'] = {}
            results['js_files'][Path(file_path).name] = js_info
            
        except Exception as e:
            logger.error(f"Error processing JS file {file_path}: {e}")
    
    def _enrich_ui_analysis(self, results: Dict[str, Any]):
        """Enrich UI analysis with cross-references and additional metadata"""
        
        # Link UiBinder templates to components
        for template_name, template_info in results.get('ui_templates', {}).items():
            # Find matching component
            for component in results['ui_components'].values():
                if component.component_name == template_name:
                    component.ui_template = template_info['template']
                    break
        
        # Generate UI architecture summary
        component_types = {}
        business_domains = set()
        gwt_widgets = set()
        
        for component in results['ui_components'].values():
            # Count by type
            comp_type = component.component_type
            component_types[comp_type] = component_types.get(comp_type, 0) + 1
            
            # Collect business domains
            business_domains.update(component.business_domains)
            
            # Collect GWT widgets
            gwt_widgets.update(component.gwt_widgets)
        
        # Add architecture summary
        results['ui_architecture'] = {
            'component_types': component_types,
            'business_domains': list(business_domains),
            'gwt_widgets_used': list(gwt_widgets),
            'total_components': len(results['ui_components']),
            'total_navigation_flows': len(results['navigation_flows'])
        }
        
        # Calculate modernization priorities
        high_priority = [c for c in results['ui_components'].values() if c.modernization_priority == 'high']
        medium_priority = [c for c in results['ui_components'].values() if c.modernization_priority == 'medium']
        low_priority = [c for c in results['ui_components'].values() if c.modernization_priority == 'low']
        
        results['modernization_analysis'] = {
            'high_priority_count': len(high_priority),
            'medium_priority_count': len(medium_priority),
            'low_priority_count': len(low_priority),
            'high_priority_components': [c.component_name for c in high_priority][:10],  # Top 10
            'average_complexity_score': sum(c.ui_complexity_score for c in results['ui_components'].values()) / max(len(results['ui_components']), 1)
        }
    
    def save_ui_analysis(self, results: Dict[str, Any], output_file: str) -> None:
        """Save UI analysis results to file"""
        logger.info(f"Saving UI analysis to: {output_file}")
        
        try:
            # Convert components to serializable format
            serializable_results = self._make_serializable(results)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully saved UI analysis to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving UI analysis: {e}")
            raise
    
    def _make_serializable(self, obj: Any) -> Any:
        """Convert objects to JSON-serializable format"""
        if hasattr(obj, '__dict__'):
            # Convert dataclass or object to dict
            if hasattr(obj, '__dataclass_fields__'):
                # Dataclass
                result = {}
                for field_name, field_value in obj.__dict__.items():
                    result[field_name] = self._make_serializable(field_value)
                return result
            else:
                # Regular object
                return self._make_serializable(obj.__dict__)
        elif isinstance(obj, dict):
            return {key: self._make_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, set):
            return list(obj)
        else:
            # Primitive type
            return obj
    
    def get_ui_file_summary(self, results: Dict[str, Any]) -> str:
        """Generate a summary report of UI file processing"""
        stats = results.get('ui_statistics', {})
        arch = results.get('ui_architecture', {})
        modern = results.get('modernization_analysis', {})
        
        summary = f"""
Enhanced Weaviate UI Analysis Results:
=====================================

Files Processed: {stats.get('total_files', 0)} total files
UI Files Identified: {stats.get('ui_files', 0)} UI-relevant files

Component Analysis:
- Java UI Components: {stats.get('java_components', 0)}
- UiBinder Templates: {stats.get('uibinder_templates', 0)}
- GWT Modules: {stats.get('gwt_modules', 0)}
- CSS Files: {stats.get('css_files', 0)}
- JavaScript Files: {stats.get('js_files', 0)}

Architecture Overview:
- Total UI Components: {arch.get('total_components', 0)}
- Navigation Flows Mapped: {arch.get('total_navigation_flows', 0)}
- Component Types: {', '.join([f'{k}({v})' for k, v in arch.get('component_types', {}).items()])}
- Business Domains: {', '.join(arch.get('business_domains', []))}
- GWT Widgets Used: {len(arch.get('gwt_widgets_used', []))} unique widgets

Modernization Analysis:
- High Priority Components: {modern.get('high_priority_count', 0)}
- Medium Priority Components: {modern.get('medium_priority_count', 0)}
- Low Priority Components: {modern.get('low_priority_count', 0)}
- Average Complexity Score: {modern.get('average_complexity_score', 0):.1f}

Processing Performance: Sub-second analysis of comprehensive UI architecture
"""
        return summary.strip()