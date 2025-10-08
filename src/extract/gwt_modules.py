"""
GWT module extraction for *.gwt.xml files.
"""
import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from lxml import etree

from config.settings import settings

logger = logging.getLogger(__name__)

class GwtModuleExtractor:
    """Extracts GWT module information from *.gwt.xml files."""
    
    def __init__(self):
        """Initialize GWT module extractor."""
        self.output_dir = settings.build_dir / "gwt_modules"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_modules(self, gwt_files: List[str]) -> List[Dict[str, Any]]:
        """Extract GWT modules from XML files."""
        modules = []
        
        for gwt_file in gwt_files:
            try:
                logger.info(f"Processing GWT module: {gwt_file}")
                module = self._extract_single_module(gwt_file)
                if module:
                    modules.append(module)
                    
                    # Save individual module JSON
                    self._save_module_json(module)
                    
            except Exception as e:
                logger.error(f"Failed to process GWT module {gwt_file}: {e}")
                continue
        
        # Save all modules JSON
        self._save_all_modules_json(modules)
        
        logger.info(f"Extracted {len(modules)} GWT modules")
        return modules
    
    def _extract_single_module(self, gwt_file: str) -> Optional[Dict[str, Any]]:
        """Extract information from a single GWT module file."""
        try:
            # Parse XML
            tree = etree.parse(gwt_file)
            root = tree.getroot()
            
            # Extract module name
            module_name = root.get('rename-to', '')
            if not module_name:
                # Try to derive from file path
                module_name = Path(gwt_file).stem
            
            # Extract inherited modules
            inherits = []
            for inherit_elem in root.findall('.//inherits'):
                inherit_name = inherit_elem.get('name', '')
                if inherit_name:
                    inherits.append(inherit_name)
            
            # Extract entry points
            entry_points = []
            for entry_point_elem in root.findall('.//entry-point'):
                entry_class = entry_point_elem.get('class', '')
                if entry_class:
                    entry_points.append(entry_class)
            
            # Extract source paths
            source_paths = []
            for source_elem in root.findall('.//source'):
                source_path = source_elem.get('path', '')
                if source_path:
                    source_paths.append(source_path)
            
            # Extract configuration properties
            config_properties = {}
            for prop_elem in root.findall('.//set-configuration-property'):
                prop_name = prop_elem.get('name', '')
                prop_value = prop_elem.get('value', '')
                if prop_name and prop_value:
                    config_properties[prop_name] = prop_value
            
            # Extract public path
            public_path = None
            public_elem = root.find('.//public')
            if public_elem is not None:
                public_path = public_elem.get('path', '')
            
            # Extract script path
            script_path = None
            script_elem = root.find('.//script')
            if script_elem is not None:
                script_path = script_elem.get('path', '')
            
            # Get raw XML content
            raw_xml = etree.tostring(root, encoding='unicode', pretty_print=True)
            
            # Create module object
            module = {
                'project': self._get_project_name(gwt_file),
                'path': gwt_file,
                'lineStart': 1,
                'lineEnd': len(raw_xml.splitlines()),
                'text': f"[GWT Module] {module_name} (entryPoints={len(entry_points)})",
                'meta': {
                    'sourcePaths': source_paths,
                    'publicPath': public_path,
                    'scriptPath': script_path,
                    'configProperties': config_properties
                },
                'moduleName': module_name,
                'inherits': inherits,
                'entryPoints': entry_points,
                'rawXml': raw_xml
            }
            
            return module
            
        except Exception as e:
            logger.error(f"Failed to extract GWT module from {gwt_file}: {e}")
            return None
    
    def _get_project_name(self, file_path: str) -> str:
        """Extract project name from file path."""
        path_parts = Path(file_path).parts
        
        # Look for common project indicators
        for part in path_parts:
            if part in ['src', 'main', 'java', 'webapp', 'resources', 'gwt']:
                continue
            if '.' in part and len(part) > 3:  # Likely a package name
                return part.split('.')[0]
            if part and not part.startswith('.') and len(part) > 2:
                return part
        
        return settings.default_project_name
    
    def _save_module_json(self, module: Dict[str, Any]):
        """Save individual module as JSON."""
        module_name = module.get('moduleName', 'unknown')
        safe_name = module_name.replace('.', '_').replace('/', '_')
        output_file = self.output_dir / f"{safe_name}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(module, f, indent=2, ensure_ascii=False)
    
    def _save_all_modules_json(self, modules: List[Dict[str, Any]]):
        """Save all modules as a single JSON file."""
        output_file = self.output_dir / "all_modules.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(modules, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(modules)} GWT modules to {output_file}")
