"""
GWT UiBinder extraction for *.ui.xml files.
"""
import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from lxml import etree

from config.settings import settings

logger = logging.getLogger(__name__)

class GwtUiBinderExtractor:
    """Extracts GWT UiBinder information from *.ui.xml files."""
    
    def __init__(self):
        """Initialize GWT UiBinder extractor."""
        self.output_dir = settings.build_dir / "gwt_uibinder"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_uibinder_files(self, ui_xml_files: List[str]) -> List[Dict[str, Any]]:
        """Extract UiBinder information from XML files."""
        uibinder_artifacts = []
        
        for ui_file in ui_xml_files:
            try:
                logger.info(f"Processing UiBinder file: {ui_file}")
                artifact = self._extract_single_uibinder(ui_file)
                if artifact:
                    uibinder_artifacts.append(artifact)
                    
                    # Save individual UiBinder JSON
                    self._save_uibinder_json(artifact)
                    
            except Exception as e:
                logger.error(f"Failed to process UiBinder file {ui_file}: {e}")
                continue
        
        # Save all UiBinder artifacts JSON
        self._save_all_uibinder_json(uibinder_artifacts)
        
        logger.info(f"Extracted {len(uibinder_artifacts)} UiBinder artifacts")
        return uibinder_artifacts
    
    def _extract_single_uibinder(self, ui_file: str) -> Optional[Dict[str, Any]]:
        """Extract information from a single UiBinder XML file."""
        try:
            # Preprocess to handle HTML entities like &nbsp; which are invalid in XML
            try:
                content = Path(ui_file).read_text(encoding='utf-8', errors='ignore')
            except Exception:
                content = ''
            if content:
                content = content.replace('&nbsp;', ' ')
                parser = etree.XMLParser(recover=True, resolve_entities=False)
                tree = etree.fromstring(content.encode('utf-8'), parser=parser)
                root = tree
            else:
                parser = etree.XMLParser(recover=True, resolve_entities=False)
                tree = etree.parse(ui_file, parser=parser)
                root = tree.getroot()
            
            # Extract owner type (usually from the root element or ui:UiBinder)
            owner_type = self._extract_owner_type(root, ui_file)
            
            # Extract widgets and fields
            widgets = self._extract_widgets(root)
            
            # Extract event handlers
            events = self._extract_events(root)
            
            # Extract i18n keys
            i18n_keys = self._extract_i18n_keys(root)
            
            # Create UiBinder artifact
            artifact = {
                'project': self._get_project_name(ui_file),
                'path': ui_file,
                'lineStart': 1,
                'lineEnd': len(etree.tostring(root, encoding='unicode').splitlines()),
                'text': f"[UiBinder] {Path(ui_file).name} (owner={owner_type})",
                'meta': {
                    'fileName': Path(ui_file).name,
                    'ownerType': owner_type
                },
                'uiXmlPath': ui_file,
                'ownerType': owner_type,
                'widgetsJson': json.dumps(widgets),
                'eventsJson': json.dumps(events),
                'i18nKeys': i18n_keys
            }
            
            return artifact
            
        except Exception as e:
            logger.error(f"Failed to extract UiBinder from {ui_file}: {e}")
            return None
    
    def _extract_owner_type(self, root, ui_file: str) -> str:
        """Extract the owner type from the UiBinder XML."""
        # Look for ui:UiBinder element
        uibinder_elem = root.find('.//{http://dl.google.com/gwt/uibinder}UiBinder')
        if uibinder_elem is not None:
            owner_type = uibinder_elem.get('type')
            if owner_type:
                return owner_type
        
        # Try to derive from file path
        file_name = Path(ui_file).stem
        if file_name.endswith('View'):
            return f"com.example.client.ui.{file_name}"
        elif file_name.endswith('Widget'):
            return f"com.example.client.widget.{file_name}"
        else:
            return f"com.example.client.ui.{file_name}"
    
    def _extract_widgets(self, root) -> List[Dict[str, str]]:
        """Extract widgets and their ui:field bindings."""
        widgets = []
        
        # Find all elements with ui:field attributes
        for elem in root.iter():
            field_name = elem.get('{http://dl.google.com/gwt/uibinder}field')
            if field_name:
                widget_type = self._get_widget_type(elem)
                widgets.append({
                    'fieldName': field_name,
                    'widgetType': widget_type,
                    'tagName': elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                })
        
        return widgets
    
    def _get_widget_type(self, elem) -> str:
        """Determine the widget type from the element."""
        tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        
        # Map common GWT widget tags to types
        widget_mapping = {
            'Button': 'Button',
            'Label': 'Label',
            'TextBox': 'TextBox',
            'TextArea': 'TextArea',
            'CheckBox': 'CheckBox',
            'RadioButton': 'RadioButton',
            'ListBox': 'ListBox',
            'Panel': 'Panel',
            'FlowPanel': 'FlowPanel',
            'VerticalPanel': 'VerticalPanel',
            'HorizontalPanel': 'HorizontalPanel',
            'Grid': 'Grid',
            'FlexTable': 'FlexTable',
            'HTML': 'HTML',
            'Image': 'Image',
            'Anchor': 'Anchor',
            'FormPanel': 'FormPanel',
            'FileUpload': 'FileUpload',
            'DateBox': 'DateBox',
            'SuggestBox': 'SuggestBox',
            'Tree': 'Tree',
            'TreeItem': 'TreeItem',
            'TabPanel': 'TabPanel',
            'TabBar': 'TabBar',
            'MenuBar': 'MenuBar',
            'MenuItem': 'MenuItem',
            'PopupPanel': 'PopupPanel',
            'DialogBox': 'DialogBox',
            'DockPanel': 'DockPanel',
            'SplitPanel': 'SplitPanel',
            'ScrollPanel': 'ScrollPanel',
            'FocusPanel': 'FocusPanel',
            'Composite': 'Composite',
            'Widget': 'Widget'
        }
        
        return widget_mapping.get(tag_name, tag_name)
    
    def _extract_events(self, root) -> List[Dict[str, str]]:
        """Extract event handlers from the UiBinder XML."""
        events = []
        
        # Common event attributes
        event_attributes = [
            'onClick', 'onDoubleClick', 'onMouseDown', 'onMouseUp', 'onMouseOver',
            'onMouseOut', 'onMouseMove', 'onKeyDown', 'onKeyUp', 'onKeyPress',
            'onFocus', 'onBlur', 'onChange', 'onLoad', 'onError'
        ]
        
        for elem in root.iter():
            for event_attr in event_attributes:
                event_handler = elem.get(event_attr)
                if event_handler:
                    # Extract field name if available
                    field_name = elem.get('{http://dl.google.com/gwt/uibinder}field', 'unknown')
                    
                    events.append({
                        'fieldName': field_name,
                        'eventType': event_attr,
                        'handlerMethod': event_handler,
                        'widgetType': self._get_widget_type(elem)
                    })
        
        return events
    
    def _extract_i18n_keys(self, root) -> List[str]:
        """Extract i18n keys from the UiBinder XML."""
        i18n_keys = []
        
        # Look for ui:with elements that reference i18n resources
        for with_elem in root.findall('.//{http://dl.google.com/gwt/uibinder}with'):
            field_name = with_elem.get('field')
            type_name = with_elem.get('type')
            
            if field_name and type_name and ('Messages' in type_name or 'Constants' in type_name):
                # This is likely an i18n resource
                i18n_keys.append(f"{field_name}:{type_name}")
        
        # Look for direct i18n key usage in text content
        for elem in root.iter():
            if elem.text and '{' in elem.text and '}' in elem.text:
                # Extract potential i18n keys from text
                import re
                keys = re.findall(r'\{([^}]+)\}', elem.text)
                i18n_keys.extend(keys)
        
        return list(set(i18n_keys))  # Remove duplicates
    
    def _get_project_name(self, file_path: str) -> str:
        """Extract project name from file path."""
        path_parts = Path(file_path).parts
        
        for part in path_parts:
            if part in ['src', 'main', 'java', 'webapp', 'resources', 'client', 'ui']:
                continue
            if '.' in part and len(part) > 3:
                return part.split('.')[0]
            if part and not part.startswith('.') and len(part) > 2:
                return part
        
        return settings.default_project_name
    
    def _save_uibinder_json(self, uibinder: Dict[str, Any]):
        """Save individual UiBinder as JSON."""
        file_name = Path(uibinder['uiXmlPath']).stem
        safe_name = file_name.replace('.', '_').replace('/', '_')
        output_file = self.output_dir / f"{safe_name}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(uibinder, f, indent=2, ensure_ascii=False)
    
    def _save_all_uibinder_json(self, uibinder_list: List[Dict[str, Any]]):
        """Save all UiBinder artifacts as a single JSON file."""
        output_file = self.output_dir / "all_uibinder.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(uibinder_list, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(uibinder_list)} UiBinder artifacts to {output_file}")
