#!/usr/bin/env python3
"""
Enhanced Output Processor
Fixes output quality issues including AI artifacts, improves data structure classification,
and enhances UI component extraction for better requirements generation.
"""

import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class UIComponent:
    """Represents a UI component extracted from GWT portlets"""
    name: str
    type: str
    widget_type: str  # Button, Grid, TextBox, etc.
    annotations: List[str]
    portlet_name: str
    business_domain: str
    interactions: List[str]  # click handlers, events, etc.

@dataclass 
class FormField:
    """Represents a form field with behavior"""
    name: str
    type: str
    required: bool
    validation_rules: List[str]
    default_value: Optional[str]
    ui_component: Optional[str]

@dataclass
class DataStructureEnhanced:
    """Enhanced data structure classification"""
    name: str
    actual_type: str  # class, interface, enum, dto
    file_path: str
    package_name: str
    fields: List[Dict[str, Any]]
    methods: List[str]
    ui_components: List[UIComponent]
    form_fields: List[FormField]
    business_domain: str
    complexity_score: int
    backend_services: List[str]
    frontend_behaviors: List[str]

class EnhancedOutputProcessor:
    """Processes and enhances analysis output quality"""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.ai_artifact_patterns = [
            r'<\|endoftext\|>.*',
            r'Human:\s*\d*\.*$',
            r'Assistant:\s*',
            r'###\s*DATA\s*###',
            r'^\s*Quantum\s*$'
        ]
        
    def clean_ai_artifacts(self, content: str) -> str:
        """Remove AI model artifacts from generated content"""
        if not content or not isinstance(content, str):
            return ""
            
        # Remove AI conversation artifacts
        for pattern in self.ai_artifact_patterns:
            content = re.sub(pattern, '', content, flags=re.MULTILINE | re.IGNORECASE)
        
        # Remove repetitive data patterns
        content = re.sub(r'(\*\*\s*(Data|Database|Design|Table|Keys)\s*\n){3,}', 
                        '**Data Management Requirements**\n', content, flags=re.MULTILINE)
        
        # Clean empty lines and normalize whitespace
        lines = [line.rstrip() for line in content.split('\n')]
        content = '\n'.join(line for line in lines if line.strip() or not lines[max(0, lines.index(line)-1):lines.index(line)+2] == ['', '', ''])
        
        return content.strip()
    
    def enhance_data_structure_classification(self, data_structures: Dict[str, Any]) -> Dict[str, Any]:
        """Improve data structure classification accuracy"""
        enhanced_structures = {
            "entities": [],
            "dtos": [],
            "enums": [],
            "interfaces": [],
            "classes": [],  # New category for properly classified classes
            "ui_components": [],  # New category for UI components
            "relationships": data_structures.get("relationships", [])
        }
        
        # Process misclassified interfaces that are actually classes
        interfaces = data_structures.get("interfaces", [])
        
        for interface in interfaces:
            # Check if this is actually a GWT Composite class (UI component)
            if self._is_gwt_composite(interface):
                ui_component = self._convert_to_ui_component(interface)
                enhanced_structures["ui_components"].append(ui_component)
                
                # Also create a proper class entry
                class_entry = self._convert_to_class(interface)
                enhanced_structures["classes"].append(class_entry)
            else:
                enhanced_structures["interfaces"].append(interface)
        
        # Copy other categories
        for category in ["entities", "dtos", "enums"]:
            enhanced_structures[category] = data_structures.get(category, [])
        
        # Update summary
        enhanced_structures["summary"] = self._generate_enhanced_summary(enhanced_structures)
        
        return enhanced_structures
    
    def _is_gwt_composite(self, interface_data: Dict[str, Any]) -> bool:
        """Check if interface is actually a GWT Composite class"""
        inheritance = interface_data.get("inheritance", "")
        annotations = interface_data.get("annotations", [])
        fields = interface_data.get("fields", [])
        
        # Check for GWT indicators
        gwt_indicators = [
            inheritance == "Composite",
            any("UiField" in str(ann) for ann in annotations),
            any("UiHandler" in str(ann) for ann in annotations),
            any(field.get("type", "").endswith("UiBinder") for field in fields),
            any(field.get("type") in ["Button", "Grid", "TextBox", "CellTree", "ScrollPanel", "DialogBox", "MenuBar"] 
                for field in fields)
        ]
        
        return any(gwt_indicators)
    
    def _convert_to_ui_component(self, interface_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert misclassified interface to UI component"""
        fields = interface_data.get("fields", [])
        
        # Extract UI widgets
        ui_widgets = []
        form_fields = []
        
        for field in fields:
            field_type = field.get("type", "")
            field_name = field.get("name", "")
            
            if field_type in ["Button", "Grid", "TextBox", "CellTree", "ScrollPanel", "DialogBox", "MenuBar"]:
                ui_widgets.append({
                    "name": field_name,
                    "widget_type": field_type,
                    "annotations": field.get("annotations", [])
                })
            
            if field_type in ["String", "Integer", "Boolean", "Date"] or field_name.endswith("Id"):
                form_fields.append({
                    "name": field_name,
                    "type": field_type,
                    "required": "required" in field_name.lower() or "id" in field_name.lower(),
                    "validation_rules": self._infer_validation_rules(field_name, field_type)
                })
        
        return {
            "name": interface_data.get("name"),
            "type": "ui_component",
            "portlet_type": "gwt_composite",
            "file_path": interface_data.get("file_path"),
            "package_name": interface_data.get("package_name"),
            "ui_widgets": ui_widgets,
            "form_fields": form_fields,
            "business_domain": interface_data.get("business_domain", ""),
            "complexity_score": len(ui_widgets) + len(form_fields) * 2,
            "interactions": self._extract_interactions(interface_data),
            "backend_services": self._infer_backend_services(interface_data),
            "frontend_behaviors": self._extract_frontend_behaviors(interface_data)
        }
    
    def _convert_to_class(self, interface_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert interface to proper class classification"""
        class_data = interface_data.copy()
        class_data["type"] = "class"
        class_data["class_type"] = "gwt_composite"
        return class_data
    
    def _infer_validation_rules(self, field_name: str, field_type: str) -> List[str]:
        """Infer validation rules from field name and type"""
        rules = []
        
        field_lower = field_name.lower()
        
        if "email" in field_lower:
            rules.append("email_format")
        if "phone" in field_lower:
            rules.append("phone_format")
        if "id" in field_lower:
            rules.extend(["required", "unique"])
        if "name" in field_lower:
            rules.append("required")
        if field_type == "String" and "password" in field_lower:
            rules.extend(["required", "min_length_8", "complexity"])
        if field_type in ["Integer", "Long", "Double"]:
            rules.append("numeric")
        
        return rules
    
    def _extract_interactions(self, interface_data: Dict[str, Any]) -> List[str]:
        """Extract user interactions from methods and annotations"""
        interactions = []
        methods = interface_data.get("methods", [])
        
        for method in methods:
            method_lower = method.lower()
            if "click" in method_lower:
                interactions.append("click_handler")
            elif "select" in method_lower:
                interactions.append("selection_handler")
            elif "load" in method_lower:
                interactions.append("data_loading")
            elif "update" in method_lower:
                interactions.append("data_update")
            elif "show" in method_lower:
                interactions.append("dialog_display")
        
        return interactions
    
    def _infer_backend_services(self, interface_data: Dict[str, Any]) -> List[str]:
        """Infer backend services needed"""
        services = []
        name = interface_data.get("name", "").lower()
        business_domain = interface_data.get("business_domain", "").lower()
        
        if "customer" in name or "customer" in business_domain:
            services.extend(["customer_service", "customer_repository", "customer_validation_service"])
        if "billing" in name or "billing" in business_domain:
            services.extend(["billing_service", "payment_service", "invoice_service"])
        if "product" in business_domain:
            services.append("product_catalog_service")
        
        return services
    
    def _extract_frontend_behaviors(self, interface_data: Dict[str, Any]) -> List[str]:
        """Extract frontend behaviors"""
        behaviors = []
        methods = interface_data.get("methods", [])
        
        method_patterns = {
            "search": "search_functionality",
            "filter": "filtering",
            "sort": "sorting",
            "page": "pagination",
            "validate": "client_validation",
            "format": "data_formatting",
            "dialog": "modal_dialogs",
            "tree": "tree_navigation"
        }
        
        for method in methods:
            for pattern, behavior in method_patterns.items():
                if pattern in method.lower():
                    behaviors.append(behavior)
        
        return behaviors
    
    def _generate_enhanced_summary(self, structures: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enhanced summary with better metrics"""
        ui_components = structures.get("ui_components", [])
        classes = structures.get("classes", [])
        
        return {
            "total_data_structures": len(structures.get("entities", [])) + len(structures.get("dtos", [])) + 
                                   len(structures.get("classes", [])) + len(structures.get("interfaces", [])),
            "total_ui_components": len(ui_components),
            "total_relationships": len(structures.get("relationships", [])),
            "ui_widgets_found": sum(len(comp.get("ui_widgets", [])) for comp in ui_components),
            "form_fields_found": sum(len(comp.get("form_fields", [])) for comp in ui_components),
            "business_domains": self._extract_business_domains(structures),
            "complexity_metrics": self._calculate_complexity_metrics(structures),
            "backend_services_needed": self._aggregate_backend_services(structures),
            "frontend_behaviors": self._aggregate_frontend_behaviors(structures)
        }
    
    def _extract_business_domains(self, structures: Dict[str, Any]) -> Dict[str, Any]:
        """Extract business domains from all structures"""
        domains = {}
        
        all_structures = []
        for category in ["entities", "dtos", "classes", "ui_components"]:
            all_structures.extend(structures.get(category, []))
        
        for struct in all_structures:
            domain = struct.get("business_domain", "")
            if domain:
                domain_parts = [d.strip() for d in domain.split(",")]
                for part in domain_parts:
                    if part:
                        domains[part] = domains.get(part, 0) + 1
        
        return domains
    
    def _calculate_complexity_metrics(self, structures: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate complexity metrics"""
        ui_components = structures.get("ui_components", [])
        complexities = [comp.get("complexity_score", 0) for comp in ui_components]
        
        if not complexities:
            return {"average_ui_complexity": 0, "max_ui_complexity": 0, "min_ui_complexity": 0}
        
        return {
            "average_ui_complexity": sum(complexities) / len(complexities),
            "max_ui_complexity": max(complexities),
            "min_ui_complexity": min(complexities),
            "total_ui_widgets": sum(len(comp.get("ui_widgets", [])) for comp in ui_components),
            "total_form_fields": sum(len(comp.get("form_fields", [])) for comp in ui_components)
        }
    
    def _aggregate_backend_services(self, structures: Dict[str, Any]) -> List[str]:
        """Aggregate all backend services needed"""
        services = set()
        
        for ui_comp in structures.get("ui_components", []):
            services.update(ui_comp.get("backend_services", []))
        
        return sorted(list(services))
    
    def _aggregate_frontend_behaviors(self, structures: Dict[str, Any]) -> List[str]:
        """Aggregate all frontend behaviors"""
        behaviors = set()
        
        for ui_comp in structures.get("ui_components", []):
            behaviors.update(ui_comp.get("frontend_behaviors", []))
        
        return sorted(list(behaviors))
    
    def fix_requirements_files(self):
        """Fix all problematic requirements files"""
        logger.info("🔧 Starting requirements file cleanup...")
        
        fixed_files = []
        error_files = []
        
        # Process traditional requirements
        trad_dir = self.output_dir / "requirements_traditional"
        if trad_dir.exists():
            for file_path in trad_dir.rglob("*.md"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_size = len(content)
                    cleaned_content = self.clean_ai_artifacts(content)
                    
                    if len(cleaned_content) < 10:  # File is essentially empty after cleaning
                        # Generate basic placeholder content
                        cleaned_content = self._generate_placeholder_content(file_path.stem)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_content)
                    
                    fixed_files.append(str(file_path))
                    logger.info(f"✅ Fixed {file_path.name}: {original_size} → {len(cleaned_content)} chars")
                    
                except Exception as e:
                    error_files.append(str(file_path))
                    logger.error(f"❌ Failed to fix {file_path.name}: {e}")
        
        return {"fixed_files": fixed_files, "error_files": error_files}
    
    def _generate_placeholder_content(self, filename: str) -> str:
        """Generate placeholder content for empty files"""
        file_type = filename.replace("_requirements", "").replace("_", " ").title()
        
        return f"""# {file_type} Requirements

**Status**: Generated placeholder - requires detailed analysis

## Overview
This document contains {file_type.lower()} requirements for the Java application analysis.

## Requirements
1. **Requirement Template**: Detailed requirements to be generated based on enhanced analysis
2. **Analysis Pending**: Full analysis requires larger codebase scope
3. **Enhancement Needed**: Current analysis limited to test files

## Notes
- This is a placeholder generated due to insufficient source data
- Enhanced analysis recommended with full application codebase
- Manual requirement gathering may be needed to supplement automated analysis

---
*Generated by Enhanced Output Processor*
"""

    def enhance_data_structures_file(self):
        """Enhance the data structures analysis file"""
        ds_file = self.output_dir / "data_structures_analysis.json"
        if not ds_file.exists():
            logger.warning("Data structures file not found")
            return
        
        try:
            with open(ds_file, 'r') as f:
                data = json.load(f)
            
            enhanced_data = self.enhance_data_structure_classification(data)
            
            # Save enhanced version
            enhanced_file = self.output_dir / "data_structures_analysis_enhanced.json"
            with open(enhanced_file, 'w') as f:
                json.dump(enhanced_data, f, indent=2)
            
            logger.info(f"✅ Enhanced data structures saved to {enhanced_file}")
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Failed to enhance data structures: {e}")
            return None

    def process_all_outputs(self):
        """Process and fix all output issues"""
        logger.info("🚀 Starting comprehensive output enhancement...")
        
        results = {
            "files_fixed": 0,
            "artifacts_removed": 0,
            "data_structures_enhanced": False,
            "ui_components_extracted": 0,
            "errors": []
        }
        
        try:
            # Fix requirements files
            fix_results = self.fix_requirements_files()
            results["files_fixed"] = len(fix_results["fixed_files"])
            results["errors"].extend(fix_results["error_files"])
            
            # Enhance data structures
            enhanced_data = self.enhance_data_structures_file()
            if enhanced_data:
                results["data_structures_enhanced"] = True
                results["ui_components_extracted"] = len(enhanced_data.get("ui_components", []))
            
            logger.info(f"✅ Output enhancement complete: {results}")
            return results
            
        except Exception as e:
            logger.error(f"❌ Output enhancement failed: {e}")
            results["errors"].append(str(e))
            return results