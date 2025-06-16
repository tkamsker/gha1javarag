import xml.etree.ElementTree as ET
from pathlib import Path
import logging
from typing import Dict, List, Optional
import os

class DoxygenParser:
    def __init__(self, xml_dir: str):
        self.xml_dir = xml_dir
        self.logger = logging.getLogger(__name__)
        
    def parse_xml_files(self) -> Dict:
        """Parse all XML files in the doxygen output directory"""
        ast_data = {
            'classes': [],
            'functions': [],
            'namespaces': [],
            'files': []
        }
        
        try:
            # Parse index.xml first to get all class references
            index_path = os.path.join(self.xml_dir, 'index.xml')
            if os.path.exists(index_path):
                self._parse_index(index_path, ast_data)
            
            # Parse individual class files
            for xml_file in Path(self.xml_dir).glob('class*.xml'):
                self._parse_class_file(xml_file, ast_data)
                
            # Parse namespace files
            for xml_file in Path(self.xml_dir).glob('namespace*.xml'):
                self._parse_namespace_file(xml_file, ast_data)
                
            return ast_data
            
        except Exception as e:
            self.logger.error(f"Error parsing doxygen XML files: {str(e)}")
            raise
            
    def _parse_index(self, index_path: str, ast_data: Dict):
        """Parse the index.xml file to get class references"""
        tree = ET.parse(index_path)
        root = tree.getroot()
        
        for compound in root.findall('.//compound'):
            compound_type = compound.get('kind')
            refid = compound.get('refid')
            
            if compound_type == 'class':
                ast_data['classes'].append({
                    'name': compound.text,
                    'refid': refid
                })
            elif compound_type == 'namespace':
                ast_data['namespaces'].append({
                    'name': compound.text,
                    'refid': refid
                })
                
    def _parse_class_file(self, xml_path: Path, ast_data: Dict):
        """Parse a class XML file to extract detailed information"""
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        compound_def = root.find('.//compounddef')
        if compound_def is None:
            return
            
        class_info = {
            'name': compound_def.findtext('compoundname', ''),
            'brief': compound_def.findtext('.//briefdescription/para', ''),
            'detailed': compound_def.findtext('.//detaileddescription/para', ''),
            'methods': [],
            'members': []
        }
        
        # Parse methods
        for member in compound_def.findall('.//memberdef[@kind="function"]'):
            method_info = {
                'name': member.findtext('name', ''),
                'type': member.findtext('type', ''),
                'args': member.findtext('argsstring', ''),
                'brief': member.findtext('.//briefdescription/para', ''),
                'detailed': member.findtext('.//detaileddescription/para', '')
            }
            class_info['methods'].append(method_info)
            
        # Parse member variables
        for member in compound_def.findall('.//memberdef[@kind="variable"]'):
            member_info = {
                'name': member.findtext('name', ''),
                'type': member.findtext('type', ''),
                'brief': member.findtext('.//briefdescription/para', '')
            }
            class_info['members'].append(member_info)
            
        ast_data['classes'].append(class_info)
        
    def _parse_namespace_file(self, xml_path: Path, ast_data: Dict):
        """Parse a namespace XML file to extract detailed information"""
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        compound_def = root.find('.//compounddef')
        if compound_def is None:
            return
            
        namespace_info = {
            'name': compound_def.findtext('compoundname', ''),
            'brief': compound_def.findtext('.//briefdescription/para', ''),
            'detailed': compound_def.findtext('.//detaileddescription/para', ''),
            'classes': [],
            'functions': []
        }
        
        # Parse contained classes
        for innerclass in compound_def.findall('.//innerclass'):
            namespace_info['classes'].append({
                'name': innerclass.text,
                'refid': innerclass.get('refid', '')
            })
            
        # Parse functions
        for member in compound_def.findall('.//memberdef[@kind="function"]'):
            function_info = {
                'name': member.findtext('name', ''),
                'type': member.findtext('type', ''),
                'args': member.findtext('argsstring', ''),
                'brief': member.findtext('.//briefdescription/para', '')
            }
            namespace_info['functions'].append(function_info)
            
        ast_data['namespaces'].append(namespace_info)
        
    def get_ast_data(self) -> Dict:
        """Get the complete AST data from doxygen XML files"""
        return self.parse_xml_files() 