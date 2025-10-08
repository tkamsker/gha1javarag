"""
JSP forms extraction for form fields and validations.
"""
import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup

from config.settings import settings

logger = logging.getLogger(__name__)

class JspFormsExtractor:
    """Extracts JSP forms and their fields."""
    
    def __init__(self):
        """Initialize JSP forms extractor."""
        self.output_dir = settings.build_dir / "jsp_forms"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_jsp_forms(self, jsp_files: List[str]) -> List[Dict[str, Any]]:
        """Extract JSP forms from JSP files."""
        forms = []
        
        for jsp_file in jsp_files:
            try:
                logger.info(f"Processing JSP file: {jsp_file}")
                file_forms = self._extract_from_single_jsp(jsp_file)
                forms.extend(file_forms)
                
            except Exception as e:
                logger.error(f"Failed to process JSP file {jsp_file}: {e}")
                continue
        
        # Save all forms JSON
        self._save_all_forms_json(forms)
        
        logger.info(f"Extracted {len(forms)} JSP forms")
        return forms
    
    def _extract_from_single_jsp(self, jsp_file: str) -> List[Dict[str, Any]]:
        """Extract forms from a single JSP file."""
        forms = []
        
        try:
            with open(jsp_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse JSP with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find all form elements
            form_elements = soup.find_all('form')
            
            for i, form_elem in enumerate(form_elements):
                form = self._extract_single_form(form_elem, jsp_file, i)
                if form:
                    forms.append(form)
                    
                    # Save individual form JSON
                    self._save_form_json(form)
            
        except Exception as e:
            logger.error(f"Failed to extract forms from JSP {jsp_file}: {e}")
        
        return forms
    
    def _extract_single_form(self, form_elem, jsp_file: str, form_index: int) -> Optional[Dict[str, Any]]:
        """Extract a single form element."""
        try:
            # Extract form attributes
            form_action = form_elem.get('action', '')
            form_method = form_elem.get('method', 'GET').upper()
            form_id = form_elem.get('id', f'form_{form_index}')
            form_name = form_elem.get('name', '')
            
            # Extract form fields
            fields = self._extract_form_fields(form_elem)
            
            # Extract validations
            validations = self._extract_form_validations(form_elem)
            
            # Create form artifact
            form = {
                'project': self._get_project_name(jsp_file),
                'path': jsp_file,
                'lineStart': 1,  # Would need to track line numbers
                'lineEnd': 100,  # Would need to track line numbers
                'text': f"[JSP Form] {form_action} ({form_method})",
                'meta': {
                    'formId': form_id,
                    'formName': form_name,
                    'formIndex': form_index
                },
                'formAction': form_action,
                'formMethod': form_method,
                'fields': fields,
                'validations': validations
            }
            
            return form
            
        except Exception as e:
            logger.error(f"Failed to extract form: {e}")
            return None
    
    def _extract_form_fields(self, form_elem) -> List[Dict[str, Any]]:
        """Extract form fields from form element."""
        fields = []
        
        # Common input field types
        input_types = ['text', 'password', 'email', 'number', 'tel', 'url', 'search', 
                      'date', 'time', 'datetime-local', 'month', 'week', 'color',
                      'checkbox', 'radio', 'file', 'hidden', 'submit', 'reset', 'button']
        
        # Extract input fields
        for input_type in input_types:
            input_elements = form_elem.find_all('input', {'type': input_type})
            for input_elem in input_elements:
                field = self._extract_input_field(input_elem, input_type)
                if field:
                    fields.append(field)
        
        # Extract select fields
        select_elements = form_elem.find_all('select')
        for select_elem in select_elements:
            field = self._extract_select_field(select_elem)
            if field:
                fields.append(field)
        
        # Extract textarea fields
        textarea_elements = form_elem.find_all('textarea')
        for textarea_elem in textarea_elements:
            field = self._extract_textarea_field(textarea_elem)
            if field:
                fields.append(field)
        
        return fields
    
    def _extract_input_field(self, input_elem, input_type: str) -> Optional[Dict[str, Any]]:
        """Extract input field information."""
        field_name = input_elem.get('name', '')
        field_id = input_elem.get('id', '')
        field_value = input_elem.get('value', '')
        field_placeholder = input_elem.get('placeholder', '')
        field_required = input_elem.has_attr('required')
        field_disabled = input_elem.has_attr('disabled')
        field_readonly = input_elem.has_attr('readonly')
        
        # Extract validation attributes
        validation_attrs = {}
        for attr in ['min', 'max', 'minlength', 'maxlength', 'pattern', 'step']:
            if input_elem.has_attr(attr):
                validation_attrs[attr] = input_elem.get(attr)
        
        return {
            'name': field_name,
            'id': field_id,
            'type': input_type,
            'value': field_value,
            'placeholder': field_placeholder,
            'required': field_required,
            'disabled': field_disabled,
            'readonly': field_readonly,
            'validation': validation_attrs
        }
    
    def _extract_select_field(self, select_elem) -> Optional[Dict[str, Any]]:
        """Extract select field information."""
        field_name = select_elem.get('name', '')
        field_id = select_elem.get('id', '')
        field_required = select_elem.has_attr('required')
        field_disabled = select_elem.has_attr('disabled')
        field_multiple = select_elem.has_attr('multiple')
        
        # Extract options
        options = []
        option_elements = select_elem.find_all('option')
        for option_elem in option_elements:
            option_value = option_elem.get('value', '')
            option_text = option_elem.get_text(strip=True)
            option_selected = option_elem.has_attr('selected')
            
            options.append({
                'value': option_value,
                'text': option_text,
                'selected': option_selected
            })
        
        return {
            'name': field_name,
            'id': field_id,
            'type': 'select',
            'required': field_required,
            'disabled': field_disabled,
            'multiple': field_multiple,
            'options': options
        }
    
    def _extract_textarea_field(self, textarea_elem) -> Optional[Dict[str, Any]]:
        """Extract textarea field information."""
        field_name = textarea_elem.get('name', '')
        field_id = textarea_elem.get('id', '')
        field_value = textarea_elem.get_text(strip=True)
        field_placeholder = textarea_elem.get('placeholder', '')
        field_required = textarea_elem.has_attr('required')
        field_disabled = textarea_elem.has_attr('disabled')
        field_readonly = textarea_elem.has_attr('readonly')
        field_rows = textarea_elem.get('rows', '')
        field_cols = textarea_elem.get('cols', '')
        
        # Extract validation attributes
        validation_attrs = {}
        for attr in ['minlength', 'maxlength']:
            if textarea_elem.has_attr(attr):
                validation_attrs[attr] = textarea_elem.get(attr)
        
        return {
            'name': field_name,
            'id': field_id,
            'type': 'textarea',
            'value': field_value,
            'placeholder': field_placeholder,
            'required': field_required,
            'disabled': field_disabled,
            'readonly': field_readonly,
            'rows': field_rows,
            'cols': field_cols,
            'validation': validation_attrs
        }
    
    def _extract_form_validations(self, form_elem) -> List[Dict[str, Any]]:
        """Extract form validation rules."""
        validations = []
        
        # Look for HTML5 validation attributes
        all_elements = form_elem.find_all(['input', 'select', 'textarea'])
        
        for elem in all_elements:
            field_name = elem.get('name', '')
            field_id = elem.get('id', '')
            
            # Extract validation attributes
            validation_rules = {}
            
            if elem.has_attr('required'):
                validation_rules['required'] = True
            
            for attr in ['min', 'max', 'minlength', 'maxlength', 'pattern']:
                if elem.has_attr(attr):
                    validation_rules[attr] = elem.get(attr)
            
            if validation_rules:
                validations.append({
                    'field': field_name or field_id,
                    'rules': validation_rules
                })
        
        # Look for JavaScript validation (simplified)
        script_elements = form_elem.find_all('script')
        for script_elem in script_elements:
            if script_elem.string:
                js_content = script_elem.string
                # Look for common validation patterns
                if 'validate' in js_content.lower() or 'required' in js_content.lower():
                    validations.append({
                        'field': 'form',
                        'rules': {'javascript': 'custom validation found'},
                        'type': 'javascript'
                    })
        
        return validations
    
    def _get_project_name(self, file_path: str) -> str:
        """Extract project name from file path."""
        path_parts = Path(file_path).parts
        
        for part in path_parts:
            if part in ['src', 'main', 'java', 'webapp', 'resources', 'jsp', 'view']:
                continue
            if '.' in part and len(part) > 3:
                return part.split('.')[0]
            if part and not part.startswith('.') and len(part) > 2:
                return part
        
        return settings.default_project_name
    
    def _save_form_json(self, form: Dict[str, Any]):
        """Save individual form as JSON."""
        form_id = form.get('meta', {}).get('formId', 'unknown')
        safe_id = form_id.replace('.', '_').replace('/', '_')
        output_file = self.output_dir / f"{safe_id}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(form, f, indent=2, ensure_ascii=False)
    
    def _save_all_forms_json(self, forms: List[Dict[str, Any]]):
        """Save all forms as a single JSON file."""
        output_file = self.output_dir / "all_forms.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(forms, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(forms)} JSP forms to {output_file}")
