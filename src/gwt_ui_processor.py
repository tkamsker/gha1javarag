"""
GWT UI Processor for Iteration 14
Extracts and analyzes GWT UI components, UiBinder templates, and navigation flows
"""

import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
import hashlib
from datetime import datetime

@dataclass
class UIField:
    """Represents a GWT @UiField"""
    field_name: str
    widget_type: str
    annotations: List[str] = field(default_factory=list)
    css_name: str = ""
    
@dataclass 
class EventHandler:
    """Represents a GWT @UiHandler"""
    method: str
    event_type: str
    annotation: str
    target_widget: str = ""
    
@dataclass
class NavigationTarget:
    """Represents navigation relationships between components"""
    target_component: str
    transition_trigger: str
    method_name: str = ""
    
@dataclass
class UIComponent:
    """Comprehensive UI component metadata"""
    component_id: str
    component_name: str
    component_type: str  # portlet, dialog, widget, view, panel
    file_path: str
    package: str
    source_code: str = ""
    ui_template: str = ""
    gwt_widgets: List[str] = field(default_factory=list)
    ui_fields: List[UIField] = field(default_factory=list)
    event_handlers: List[EventHandler] = field(default_factory=list)
    business_domains: List[str] = field(default_factory=list)
    user_roles: List[str] = field(default_factory=list)
    navigation_targets: List[NavigationTarget] = field(default_factory=list)
    ui_complexity_score: int = 0
    accessibility_features: List[str] = field(default_factory=list)
    responsive_design: bool = False
    performance_notes: str = ""
    modernization_priority: str = "medium"
    migration_complexity: str = "medium"
    
@dataclass
class NavigationFlow:
    """Represents user navigation patterns and workflows"""
    flow_id: str
    flow_name: str
    flow_description: str
    source_component: str
    target_component: str
    transition_trigger: str
    user_role: str = ""
    business_process: str = ""
    flow_complexity: int = 1
    usage_frequency: str = "unknown"
    modernization_recommendation: str = ""

class GWTUIProcessor:
    """Main processor for GWT UI components and navigation flows"""
    
    def __init__(self):
        self.ui_components: Dict[str, UIComponent] = {}
        self.navigation_flows: List[NavigationFlow] = []
        
        # GWT widget patterns
        self.gwt_widgets = {
            'ScrollPanel', 'CellTree', 'RadioButton', 'CheckBox', 'Button',
            'TextBox', 'TextArea', 'PasswordTextBox', 'ListBox', 'SuggestBox',
            'Tree', 'TreeItem', 'MenuBar', 'MenuItem', 'TabPanel', 'DeckPanel',
            'StackPanel', 'DisclosurePanel', 'DialogBox', 'PopupPanel',
            'HorizontalPanel', 'VerticalPanel', 'FlowPanel', 'DockPanel',
            'HTMLPanel', 'Grid', 'FlexTable', 'FormPanel', 'FileUpload',
            'Image', 'Label', 'HTML', 'Hyperlink', 'Frame', 'DatePicker',
            'ToggleButton', 'PushButton', 'Anchor', 'InlineLabel'
        }
        
        # Business domain keywords
        self.domain_keywords = {
            'customer': ['customer', 'party', 'client', 'user', 'account'],
            'product': ['product', 'service', 'catalog', 'offer', 'subscription'],
            'billing': ['billing', 'invoice', 'payment', 'price', 'tariff', 'charge'],
            'order': ['order', 'purchase', 'buy', 'cart', 'checkout'],
            'support': ['support', 'ticket', 'help', 'issue', 'problem', 'resolve'],
            'admin': ['admin', 'administration', 'config', 'setting', 'management'],
            'network': ['network', 'bandwidth', 'connection', 'provisioning']
        }
        
    def parse_gwt_component(self, java_file_path: str) -> Optional[UIComponent]:
        """Parse a GWT Java component file"""
        try:
            with open(java_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract basic component info
            component_name = Path(java_file_path).stem
            package = self._extract_package(content)
            component_type = self._determine_component_type(component_name, content)
            
            if not self._is_ui_component(content):
                return None
                
            # Generate unique component ID
            component_id = hashlib.md5(f"{package}.{component_name}".encode()).hexdigest()[:12]
            
            component = UIComponent(
                component_id=component_id,
                component_name=component_name,
                component_type=component_type,
                file_path=java_file_path,
                package=package,
                source_code=content
            )
            
            # Extract UI-specific metadata
            component.gwt_widgets = self._extract_gwt_widgets(content)
            component.ui_fields = self._extract_ui_fields(content)
            component.event_handlers = self._extract_event_handlers(content)
            component.business_domains = self._extract_business_domains(content)
            component.user_roles = self._extract_user_roles(content)
            component.navigation_targets = self._extract_navigation_targets(content)
            component.ui_complexity_score = self._calculate_complexity_score(component)
            component.accessibility_features = self._analyze_accessibility_features(content)
            component.responsive_design = self._check_responsive_design(content)
            component.performance_notes = self._analyze_performance_characteristics(content)
            component.modernization_priority = self._assess_modernization_priority(component)
            component.migration_complexity = self._assess_migration_complexity(component)
            
            return component
            
        except Exception as e:
            print(f"Error parsing GWT component {java_file_path}: {e}")
            return None
    
    def parse_uibinder_template(self, xml_file_path: str) -> Optional[str]:
        """Parse UiBinder XML template"""
        try:
            with open(xml_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse XML structure
            root = ET.fromstring(content)
            
            # Extract widget hierarchy
            template_info = {
                'widgets': self._extract_xml_widgets(root),
                'layout': self._analyze_layout_structure(root),
                'styling': self._extract_css_references(content),
                'data_binding': self._extract_data_binding(content)
            }
            
            return json.dumps(template_info, indent=2)
            
        except Exception as e:
            print(f"Error parsing UiBinder template {xml_file_path}: {e}")
            return None
    
    def analyze_navigation_flow(self, components: Dict[str, UIComponent]) -> List[NavigationFlow]:
        """Analyze navigation flows between components"""
        flows = []
        
        for comp_id, component in components.items():
            for nav_target in component.navigation_targets:
                flow_id = hashlib.md5(f"{component.component_name}->{nav_target.target_component}".encode()).hexdigest()[:12]
                
                flow = NavigationFlow(
                    flow_id=flow_id,
                    flow_name=f"{component.component_name} to {nav_target.target_component}",
                    flow_description=f"Navigation from {component.component_type} to target component",
                    source_component=component.component_name,
                    target_component=nav_target.target_component,
                    transition_trigger=nav_target.transition_trigger,
                    user_role=self._infer_user_role(component),
                    business_process=self._infer_business_process(component),
                    flow_complexity=self._calculate_flow_complexity(component, nav_target),
                    modernization_recommendation=self._generate_flow_modernization_recommendation(component, nav_target)
                )
                
                flows.append(flow)
        
        return flows
    
    def _extract_package(self, content: str) -> str:
        """Extract package declaration"""
        match = re.search(r'package\s+([^;]+);', content)
        return match.group(1) if match else ""
    
    def _determine_component_type(self, component_name: str, content: str) -> str:
        """Determine the type of UI component"""
        name_lower = component_name.lower()
        
        if 'portlet' in name_lower:
            return 'portlet'
        elif 'dialog' in name_lower:
            return 'dialog'
        elif 'view' in name_lower:
            return 'view'
        elif 'panel' in name_lower:
            return 'panel'
        elif 'widget' in name_lower:
            return 'widget'
        elif re.search(r'extends\s+Composite', content):
            return 'composite'
        elif re.search(r'extends\s+DialogBox', content):
            return 'dialog'
        elif re.search(r'extends\s+PopupPanel', content):
            return 'popup'
        else:
            return 'component'
    
    def _is_ui_component(self, content: str) -> bool:
        """Check if the file is a UI component"""
        ui_indicators = [
            '@UiField', '@UiHandler', '@UiTemplate',
            'extends Composite', 'extends DialogBox', 'extends PopupPanel',
            'UiBinder', 'Widget', 'Panel'
        ]
        
        return any(indicator in content for indicator in ui_indicators)
    
    def _extract_gwt_widgets(self, content: str) -> List[str]:
        """Extract GWT widgets used in the component"""
        found_widgets = []
        
        for widget in self.gwt_widgets:
            if re.search(rf'\b{widget}\b', content):
                found_widgets.append(widget)
        
        # Also look for @UiField declarations
        ui_field_pattern = r'@UiField\s+(\w+)\s+(\w+);'
        for match in re.finditer(ui_field_pattern, content):
            widget_type = match.group(1)
            if widget_type in self.gwt_widgets:
                found_widgets.append(widget_type)
        
        return list(set(found_widgets))
    
    def _extract_ui_fields(self, content: str) -> List[UIField]:
        """Extract @UiField declarations"""
        ui_fields = []
        
        # Pattern for @UiField declarations
        pattern = r'@UiField(?:\([^)]*\))?\s+(\w+)\s+(\w+);'
        
        for match in re.finditer(pattern, content):
            widget_type = match.group(1)
            field_name = match.group(2)
            
            ui_field = UIField(
                field_name=field_name,
                widget_type=widget_type,
                annotations=['@UiField']
            )
            ui_fields.append(ui_field)
        
        return ui_fields
    
    def _extract_event_handlers(self, content: str) -> List[EventHandler]:
        """Extract @UiHandler declarations"""
        handlers = []
        
        # Pattern for @UiHandler methods
        pattern = r'@UiHandler\(["\']([^"\']+)["\']\)\s+(?:public\s+)?void\s+(\w+)\s*\([^)]*(\w+Event)[^)]*\)'
        
        for match in re.finditer(pattern, content):
            target_widget = match.group(1)
            method_name = match.group(2)
            event_type = match.group(3)
            annotation = match.group(0).split('\n')[0].strip()
            
            handler = EventHandler(
                method=method_name,
                event_type=event_type,
                annotation=annotation,
                target_widget=target_widget
            )
            handlers.append(handler)
        
        return handlers
    
    def _extract_business_domains(self, content: str) -> List[str]:
        """Extract business domains based on keywords"""
        domains = []
        content_lower = content.lower()
        
        for domain, keywords in self.domain_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                domains.append(domain)
        
        return domains
    
    def _extract_user_roles(self, content: str) -> List[str]:
        """Extract user roles from component context"""
        roles = []
        content_lower = content.lower()
        
        role_patterns = {
            'administrator': ['admin', 'administrator', 'management'],
            'user': ['user', 'customer', 'client'],
            'operator': ['operator', 'agent', 'support'],
            'manager': ['manager', 'supervisor', 'lead']
        }
        
        for role, patterns in role_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                roles.append(role)
        
        return roles if roles else ['user']  # Default to 'user'
    
    def _extract_navigation_targets(self, content: str) -> List[NavigationTarget]:
        """Extract navigation targets and transitions"""
        targets = []
        
        # Look for common navigation patterns
        patterns = [
            r'show\(\s*new\s+(\w+)\(',  # show(new Dialog())
            r'\.show\(\s*(\w+)',        # component.show()
            r'History\.newItem\(["\']([^"\']+)["\']\)',  # History navigation
            r'Window\.open\(["\']([^"\']+)["\']\)',      # Window.open()
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                target = match.group(1)
                
                nav_target = NavigationTarget(
                    target_component=target,
                    transition_trigger="programmatic"
                )
                targets.append(nav_target)
        
        return targets
    
    def _calculate_complexity_score(self, component: UIComponent) -> int:
        """Calculate UI complexity score"""
        score = 0
        
        # Base score
        score += 10
        
        # Widget complexity
        score += len(component.gwt_widgets) * 2
        
        # UI fields complexity
        score += len(component.ui_fields) * 3
        
        # Event handlers complexity
        score += len(component.event_handlers) * 5
        
        # Navigation complexity
        score += len(component.navigation_targets) * 4
        
        # Business domain complexity
        score += len(component.business_domains) * 2
        
        return min(score, 100)  # Cap at 100
    
    def _analyze_accessibility_features(self, content: str) -> List[str]:
        """Analyze accessibility features"""
        features = []
        
        accessibility_patterns = {
            'aria_labels': r'setAriaLabel|aria-label',
            'keyboard_navigation': r'KeyboardListener|onKeyDown|onKeyUp|onKeyPress',
            'focus_management': r'setFocus|focus\(\)',
            'alt_text': r'setAltText|alt=',
            'role_attributes': r'role=|setRole'
        }
        
        for feature, pattern in accessibility_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                features.append(feature)
        
        return features
    
    def _check_responsive_design(self, content: str) -> bool:
        """Check for responsive design indicators"""
        responsive_patterns = [
            r'@media',
            r'getOffsetWidth',
            r'Window\.getClientWidth',
            r'ResizeLayoutPanel',
            r'responsive',
            r'mobile'
        ]
        
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in responsive_patterns)
    
    def _analyze_performance_characteristics(self, content: str) -> str:
        """Analyze performance characteristics"""
        notes = []
        
        if 'CellTree' in content or 'Tree' in content:
            notes.append("Tree widget - consider virtualization for large datasets")
        
        if 'FlexTable' in content or 'Grid' in content:
            notes.append("Table widget - implement pagination for performance")
        
        if len(re.findall(r'@UiField', content)) > 20:
            notes.append("High number of UI fields - consider component decomposition")
        
        if 'Timer' in content:
            notes.append("Uses timers - verify cleanup on component destruction")
        
        return "; ".join(notes) if notes else "Standard performance characteristics"
    
    def _assess_modernization_priority(self, component: UIComponent) -> str:
        """Assess modernization priority"""
        score = 0
        
        # High complexity = higher priority
        if component.ui_complexity_score > 70:
            score += 3
        elif component.ui_complexity_score > 40:
            score += 2
        else:
            score += 1
        
        # Critical business domains = higher priority
        critical_domains = {'customer', 'billing', 'order'}
        if any(domain in critical_domains for domain in component.business_domains):
            score += 2
        
        # Poor accessibility = higher priority
        if not component.accessibility_features:
            score += 2
        
        # Not responsive = higher priority
        if not component.responsive_design:
            score += 1
        
        if score >= 6:
            return "high"
        elif score >= 4:
            return "medium"
        else:
            return "low"
    
    def _assess_migration_complexity(self, component: UIComponent) -> str:
        """Assess migration complexity to modern frameworks"""
        complexity_score = 0
        
        # Component type complexity
        type_complexity = {
            'portlet': 3,
            'dialog': 2,
            'view': 2,
            'panel': 1,
            'widget': 1,
            'composite': 2
        }
        complexity_score += type_complexity.get(component.component_type, 1)
        
        # Widget complexity
        complex_widgets = {'CellTree', 'Tree', 'FlexTable', 'MenuBar'}
        if any(widget in complex_widgets for widget in component.gwt_widgets):
            complexity_score += 2
        
        # Event handler complexity
        if len(component.event_handlers) > 10:
            complexity_score += 2
        elif len(component.event_handlers) > 5:
            complexity_score += 1
        
        # Navigation complexity
        if len(component.navigation_targets) > 5:
            complexity_score += 2
        
        if complexity_score >= 7:
            return "high"
        elif complexity_score >= 4:
            return "medium"
        else:
            return "low"
    
    def _extract_xml_widgets(self, root: ET.Element) -> List[str]:
        """Extract widgets from XML structure"""
        widgets = []
        
        def traverse(element):
            if element.tag.startswith('g:') or element.tag.startswith('ui:'):
                widget_name = element.tag.split(':')[1]
                if widget_name in self.gwt_widgets:
                    widgets.append(widget_name)
            
            for child in element:
                traverse(child)
        
        traverse(root)
        return list(set(widgets))
    
    def _analyze_layout_structure(self, root: ET.Element) -> str:
        """Analyze layout structure from XML"""
        layout_types = []
        
        def find_layouts(element):
            if 'Panel' in element.tag:
                layout_types.append(element.tag)
            for child in element:
                find_layouts(child)
        
        find_layouts(root)
        return ", ".join(set(layout_types)) if layout_types else "No specific layout"
    
    def _extract_css_references(self, content: str) -> List[str]:
        """Extract CSS class references"""
        css_pattern = r'addStyleName\(["\']([^"\']+)["\']\)|styleName=["\']([^"\']+)["\']\)'
        matches = re.findall(css_pattern, content)
        
        css_classes = []
        for match in matches:
            css_classes.extend([m for m in match if m])
        
        return list(set(css_classes))
    
    def _extract_data_binding(self, content: str) -> List[str]:
        """Extract data binding expressions"""
        binding_pattern = r'\{[^}]+\}'
        return re.findall(binding_pattern, content)
    
    def _infer_user_role(self, component: UIComponent) -> str:
        """Infer user role from component"""
        if component.user_roles:
            return component.user_roles[0]
        return "user"
    
    def _infer_business_process(self, component: UIComponent) -> str:
        """Infer business process from component"""
        if component.business_domains:
            domain = component.business_domains[0]
            return f"{domain}_management"
        return "general_process"
    
    def _calculate_flow_complexity(self, component: UIComponent, nav_target: NavigationTarget) -> int:
        """Calculate navigation flow complexity"""
        base_complexity = 1
        
        # Add complexity based on component type
        if component.component_type in ['portlet', 'dialog']:
            base_complexity += 2
        elif component.component_type == 'view':
            base_complexity += 1
        
        # Add complexity for number of event handlers
        base_complexity += min(len(component.event_handlers) // 5, 3)
        
        return base_complexity
    
    def _generate_flow_modernization_recommendation(self, component: UIComponent, nav_target: NavigationTarget) -> str:
        """Generate modernization recommendations for navigation flows"""
        recommendations = []
        
        if component.component_type == 'dialog':
            recommendations.append("Consider modal components with modern frameworks")
        
        if not component.responsive_design:
            recommendations.append("Implement responsive navigation patterns")
        
        if len(component.event_handlers) > 10:
            recommendations.append("Simplify event handling with modern state management")
        
        return "; ".join(recommendations) if recommendations else "Standard modernization approach"

    def process_ui_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """Process multiple UI files and return comprehensive results"""
        results = {
            'ui_components': {},
            'navigation_flows': [],
            'summary': {
                'total_files_processed': 0,
                'ui_components_found': 0,
                'navigation_flows_mapped': 0,
                'gwt_widgets_cataloged': set(),
                'business_domains_identified': set(),
                'processing_timestamp': datetime.now().isoformat()
            }
        }
        
        # Process Java files
        for file_path in file_paths:
            if file_path.endswith('.java'):
                component = self.parse_gwt_component(file_path)
                if component:
                    results['ui_components'][component.component_id] = component
                    results['summary']['gwt_widgets_cataloged'].update(component.gwt_widgets)
                    results['summary']['business_domains_identified'].update(component.business_domains)
        
        # Process UiBinder templates
        for file_path in file_paths:
            if file_path.endswith('.ui.xml'):
                template = self.parse_uibinder_template(file_path)
                if template:
                    # Find corresponding Java component
                    component_name = Path(file_path).stem
                    for comp in results['ui_components'].values():
                        if comp.component_name == component_name:
                            comp.ui_template = template
                            break
        
        # Analyze navigation flows
        results['navigation_flows'] = self.analyze_navigation_flow(results['ui_components'])
        
        # Update summary
        results['summary']['total_files_processed'] = len(file_paths)
        results['summary']['ui_components_found'] = len(results['ui_components'])
        results['summary']['navigation_flows_mapped'] = len(results['navigation_flows'])
        results['summary']['gwt_widgets_cataloged'] = list(results['summary']['gwt_widgets_cataloged'])
        results['summary']['business_domains_identified'] = list(results['summary']['business_domains_identified'])
        
        return results