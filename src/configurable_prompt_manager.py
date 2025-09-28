#!/usr/bin/env python3
"""
Configurable Prompt Manager for Requirements Generation

This module provides centralized management of all prompts used for AI-powered 
requirements generation, allowing easy modification and customization through
JSON and Markdown files.
"""

import json
import os
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ConfigurablePromptManager:
    """Manages configurable prompts for requirements generation"""
    
    def __init__(self, prompts_dir: str = "./prompts"):
        """
        Initialize the prompt manager
        
        Args:
            prompts_dir: Directory containing prompt configuration files
        """
        self.prompts_dir = Path(prompts_dir)
        self.prompts_config = {}
        self.artifact_cleanup_patterns = []
        self.prompt_settings = {}
        
        # Ensure prompts directory exists
        self.prompts_dir.mkdir(exist_ok=True)
        
        # Load configurations
        self._load_prompt_configurations()
        
    def _load_prompt_configurations(self):
        """Load all prompt configurations from files"""
        try:
            # Load main requirements prompts
            requirements_file = self.prompts_dir / "requirements_prompts.json"
            if requirements_file.exists():
                with open(requirements_file, 'r') as f:
                    config = json.load(f)
                    self.prompts_config = config
                    self.artifact_cleanup_patterns = config.get("ai_artifact_cleanup_patterns", [])
                    self.prompt_settings = config.get("prompt_settings", {})
                    logger.info(f"Loaded prompts from {requirements_file}")
            else:
                logger.warning(f"Requirements prompts file not found: {requirements_file}")
                
            # Load additional prompt files
            for prompt_file in self.prompts_dir.glob("*.md"):
                self._load_markdown_prompts(prompt_file)
                
        except Exception as e:
            logger.error(f"Error loading prompt configurations: {e}")
            
    def _load_markdown_prompts(self, file_path: Path):
        """Load prompts from markdown files"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # Extract prompts from markdown code blocks
                prompts = self._extract_prompts_from_markdown(content)
                for prompt_name, prompt_content in prompts.items():
                    self.prompts_config[prompt_name] = {
                        "template": prompt_content,
                        "source_file": str(file_path)
                    }
                logger.info(f"Loaded markdown prompts from {file_path}")
        except Exception as e:
            logger.error(f"Error loading markdown prompts from {file_path}: {e}")
            
    def _extract_prompts_from_markdown(self, content: str) -> Dict[str, str]:
        """Extract prompt templates from markdown code blocks"""
        prompts = {}
        
        # Find code blocks with prompt content
        code_block_pattern = r'```(?:\w+)?\n(.*?)\n```'
        matches = re.findall(code_block_pattern, content, re.DOTALL)
        
        # Extract prompts based on headers
        sections = re.split(r'^## (.+)$', content, flags=re.MULTILINE)
        
        for i in range(1, len(sections), 2):
            section_name = sections[i].strip().lower().replace(' ', '_')
            section_content = sections[i + 1] if i + 1 < len(sections) else ""
            
            # Extract the main prompt from code blocks in this section
            code_matches = re.findall(code_block_pattern, section_content, re.DOTALL)
            if code_matches:
                prompts[section_name] = code_matches[0].strip()
                
        return prompts
        
    def get_prompt_template(self, prompt_type: str) -> str:
        """
        Get a prompt template by type
        
        Args:
            prompt_type: Type of prompt (e.g., 'data_layer_requirements')
            
        Returns:
            Prompt template string
        """
        if prompt_type in self.prompts_config:
            return self.prompts_config[prompt_type].get("template", "")
        
        logger.warning(f"Prompt template not found: {prompt_type}")
        return f"Generate {prompt_type.replace('_', ' ')} based on the following context:\n{{context}}"
        
    def format_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        Format a prompt template with provided parameters
        
        Args:
            prompt_type: Type of prompt template
            **kwargs: Parameters to substitute in the template
            
        Returns:
            Formatted prompt string
        """
        template = self.get_prompt_template(prompt_type)
        
        try:
            formatted_prompt = template.format(**kwargs)
            return formatted_prompt
        except KeyError as e:
            logger.error(f"Missing parameter for prompt {prompt_type}: {e}")
            return template
        except Exception as e:
            logger.error(f"Error formatting prompt {prompt_type}: {e}")
            return template
            
    def get_cleanup_patterns(self) -> List[Dict[str, str]]:
        """Get AI artifact cleanup patterns"""
        return self.artifact_cleanup_patterns
        
    def get_prompt_settings(self) -> Dict[str, Any]:
        """Get AI model settings for prompts"""
        return self.prompt_settings
        
    def clean_ai_artifacts(self, text: str) -> str:
        """
        Clean AI artifacts from generated text using configured patterns
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        cleaned_text = text
        
        for pattern_config in self.artifact_cleanup_patterns:
            pattern = pattern_config.get("pattern", "")
            replacement = pattern_config.get("replacement", "")
            
            try:
                cleaned_text = re.sub(pattern, replacement, cleaned_text, flags=re.MULTILINE | re.IGNORECASE)
            except re.error as e:
                logger.error(f"Invalid regex pattern '{pattern}': {e}")
                continue
                
        # Additional cleanup
        cleaned_text = self._additional_cleanup(cleaned_text)
        
        return cleaned_text.strip()
        
    def _additional_cleanup(self, text: str) -> str:
        """Perform additional text cleanup"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Remove lines that are mostly repetitive characters
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip lines with excessive repetitive patterns
            if re.search(r'(.)\1{20,}', line):  # Same character repeated 20+ times
                continue
            if re.search(r'(\d\.){10,}', line):  # "1.2.3.4..." pattern
                continue
            if re.search(r'([\w\s]{1,3})\1{10,}', line):  # Short patterns repeated
                continue
            # Skip lines with excessive dash-separated fragments
            if re.search(r'(\s+-\s+[^-\n]{0,15}){8,}', line):
                continue
            # Skip lines that are mostly fragments without substance
            if len(line.strip()) > 0 and line.count(' - ') > 8 and len(line) > 200:
                continue
                
            cleaned_lines.append(line)
            
        return '\n'.join(cleaned_lines)
        
    def aggressive_model_cleanup(self, text: str) -> str:
        """
        Perform aggressive cleanup for models with severe artifact issues
        """
        # First do standard cleanup
        text = self.clean_ai_artifacts(text)
        
        # Additional aggressive patterns for problematic models
        aggressive_patterns = [
            # Remove conversation artifacts that leak through
            (r'<\|[^|]*\|>[^\\n]*', ''),
            (r'Human:\s*[^\\n]*', ''),
            (r'Assistant:\s*[^\\n]*', ''),
            
            # Clean up fragmented content
            (r'(\s+-\s+[^-\n]{0,20}){6,}', ''),  # Excessive dash-separated fragments
            (r'(VARCHAR\([^)]*\)\s*-\s*){3,}', 'VARCHAR(255) '),  # Repeated SQL type fragments
            (r'(NOT NULL\s*-\s*){2,}', 'NOT NULL '),  # Repeated constraint fragments
            (r'(created_at\s*-\s*TIMESTAMP\s*-\s*updated_at\s*-\s*deleted_at\s*-\s*status\s*-\s*deleted_at\s*){2,}', 'created_at TIMESTAMP, updated_at TIMESTAMP, deleted_at TIMESTAMP, status VARCHAR(50)'),
            
            # Remove excessive repetitive SQL structure patterns
            (r'(\w+_id\s*-\s*){3,}', ''),
            (r'(deleted_at\s*-\s*){3,}', 'deleted_at TIMESTAMP, '),
            
            # Clean up malformed content
            (r'-\s*-\s*-\s*-\s*-\s*', '- '),  # Multiple dashes
            (r'\*\*([^*]+)\*\*\s*\(([^)]+)\s*\(\s*', '**$1** ($2) '),  # Fix malformed bold with parens
        ]
        
        for pattern, replacement in aggressive_patterns:
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE | re.IGNORECASE)
        
        # Final structural cleanup
        lines = text.split('\n')
        final_lines = []
        prev_line_empty = False
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines after empty lines (max 1 blank line)
            if not line:
                if not prev_line_empty:
                    final_lines.append('')
                    prev_line_empty = True
                continue
            
            prev_line_empty = False
            
            # Skip lines that are just fragments or malformed
            if len(line) < 10 and line.count('-') > len(line) // 3:
                continue
            
            final_lines.append(line)
        
        return '\n'.join(final_lines).strip()
        
    def validate_output(self, text: str) -> tuple[bool, List[str]]:
        """
        Validate generated output for quality and cleanliness
        
        Args:
            text: Generated text to validate
            
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Check for AI artifacts
        artifact_patterns = [
            r'<\|endoftext\|>',
            r'Human:\s*\d*',
            r'Assistant:',
            r'###\s*DATA\s*###',
            r'Quantum\s+'
        ]
        
        for pattern in artifact_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                issues.append(f"Contains AI artifact pattern: {pattern}")
                
        # Check for repetitive corruption
        if re.search(r'(.)\1{50,}', text):
            issues.append("Contains excessive character repetition")
            
        if re.search(r'(\d\.){20,}', text):
            issues.append("Contains repetitive number patterns")
            
        # Check for minimum content quality
        if len(text.strip()) < 100:
            issues.append("Content too short - possible generation failure")
            
        if text.count('\n') < 5:
            issues.append("Insufficient structure - possible formatting issue")
            
        return len(issues) == 0, issues
        
    def create_data_structure_prompt(self, 
                                   code_content: str, 
                                   analysis_type: str = "comprehensive") -> str:
        """
        Create a specialized prompt for data structure analysis
        
        Args:
            code_content: Java/JSP code to analyze
            analysis_type: Type of analysis (comprehensive, fields_only, ui_only)
            
        Returns:
            Formatted prompt for data structure analysis
        """
        if analysis_type == "comprehensive":
            return self.format_prompt("field_analysis_prompt", code_content=code_content)
        elif analysis_type == "ui_only":
            return self.format_prompt("ui_component_analysis_prompt", code_content=code_content)
        else:
            # Fallback to basic analysis
            return f"""
Analyze the following code and extract all data structures, fields, and their properties:

{code_content}

Focus on:
1. Class definitions and field declarations
2. Form fields and UI components
3. Validation rules and annotations
4. Database mapping requirements

Provide structured output in JSON format. Do not include conversation artifacts.
"""

    def reload_configurations(self):
        """Reload all prompt configurations from files"""
        self.prompts_config = {}
        self.artifact_cleanup_patterns = []
        self.prompt_settings = {}
        self._load_prompt_configurations()
        logger.info("Prompt configurations reloaded")
        
    def save_prompt_template(self, prompt_type: str, template: str, description: str = ""):
        """
        Save a new prompt template to the configuration
        
        Args:
            prompt_type: Type identifier for the prompt
            template: Prompt template content
            description: Description of the prompt purpose
        """
        self.prompts_config[prompt_type] = {
            "template": template,
            "description": description
        }
        
        # Save to file
        try:
            requirements_file = self.prompts_dir / "requirements_prompts.json"
            config_data = {
                **self.prompts_config,
                "ai_artifact_cleanup_patterns": self.artifact_cleanup_patterns,
                "prompt_settings": self.prompt_settings
            }
            
            with open(requirements_file, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            logger.info(f"Saved prompt template: {prompt_type}")
        except Exception as e:
            logger.error(f"Error saving prompt template: {e}")


# Global instance for easy access
_prompt_manager = None

def get_prompt_manager(prompts_dir: str = "./prompts") -> ConfigurablePromptManager:
    """Get or create global prompt manager instance"""
    global _prompt_manager
    if _prompt_manager is None:
        _prompt_manager = ConfigurablePromptManager(prompts_dir)
    return _prompt_manager

def clean_ai_response(text: str) -> str:
    """Convenience function to clean AI artifacts"""
    manager = get_prompt_manager()
    return manager.clean_ai_artifacts(text)

def validate_ai_response(text: str) -> tuple[bool, List[str]]:
    """Convenience function to validate AI response quality"""
    manager = get_prompt_manager()
    return manager.validate_output(text)