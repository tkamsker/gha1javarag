"""
HTML/HTM file extractor for frontend analysis.
Extracts GWT features, forms, scripts, and other frontend artifacts from HTML files.
"""
import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from html.parser import HTMLParser
from html import unescape

from config.settings import settings
from config.project_utils import extract_project_name_from_path

logger = logging.getLogger(__name__)


class GwtHtmlParser(HTMLParser):
    """HTML parser that extracts GWT-specific features and frontend artifacts."""
    
    def __init__(self):
        super().__init__()
        self.gwt_features: List[Dict[str, Any]] = []
        self.scripts: List[Dict[str, str]] = []
        self.forms: List[Dict[str, Any]] = []
        self.links: List[Dict[str, str]] = []
        self.meta_tags: List[Dict[str, str]] = []
        self.gwt_modules: Set[str] = set()
        self.gwt_nocache: Set[str] = set()
        self.current_form: Optional[Dict[str, Any]] = None
        self.current_tag: Optional[str] = None
        self.current_attrs: Dict[str, str] = {}
        
    def handle_starttag(self, tag: str, attrs: list):
        """Handle opening HTML tags."""
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        
        # Extract GWT module references
        if tag == 'script' and self.current_attrs.get('src'):
            src = self.current_attrs['src']
            # Look for GWT module patterns
            if '.nocache.js' in src or 'gwt' in src.lower():
                self.gwt_nocache.add(src)
                self.gwt_features.append({
                    'type': 'gwt_nocache_script',
                    'src': src,
                    'attrs': self.current_attrs
                })
            # Extract module name from path
            module_match = re.search(r'([\w\.]+)\.nocache\.js', src)
            if module_match:
                self.gwt_modules.add(module_match.group(1))
        
        # Extract all scripts
        if tag == 'script':
            script_info = {
                'type': self.current_attrs.get('type', 'text/javascript'),
                'src': self.current_attrs.get('src', ''),
                'id': self.current_attrs.get('id', ''),
                'attrs': self.current_attrs
            }
            self.scripts.append(script_info)
        
        # Extract forms
        if tag == 'form':
            self.current_form = {
                'action': self.current_attrs.get('action', ''),
                'method': self.current_attrs.get('method', 'GET').upper(),
                'id': self.current_attrs.get('id', ''),
                'name': self.current_attrs.get('name', ''),
                'enctype': self.current_attrs.get('enctype', ''),
                'fields': [],
                'attrs': self.current_attrs
            }
        
        # Extract form fields
        if self.current_form and tag in ['input', 'select', 'textarea', 'button']:
            field = {
                'type': self.current_attrs.get('type', tag),
                'name': self.current_attrs.get('name', ''),
                'id': self.current_attrs.get('id', ''),
                'value': self.current_attrs.get('value', ''),
                'placeholder': self.current_attrs.get('placeholder', ''),
                'required': 'required' in self.current_attrs,
                'attrs': self.current_attrs
            }
            self.current_form['fields'].append(field)
        
        # Extract links
        if tag == 'a':
            link_info = {
                'href': self.current_attrs.get('href', ''),
                'id': self.current_attrs.get('id', ''),
                'class': self.current_attrs.get('class', ''),
                'attrs': self.current_attrs
            }
            self.links.append(link_info)
        
        # Extract meta tags
        if tag == 'meta':
            meta_info = {
                'name': self.current_attrs.get('name', ''),
                'property': self.current_attrs.get('property', ''),
                'content': self.current_attrs.get('content', ''),
                'http-equiv': self.current_attrs.get('http-equiv', ''),
                'attrs': self.current_attrs
            }
            self.meta_tags.append(meta_info)
    
    def handle_endtag(self, tag: str):
        """Handle closing HTML tags."""
        if tag == 'form' and self.current_form:
            self.forms.append(self.current_form)
            self.current_form = None
        self.current_tag = None
        self.current_attrs = {}
    
    def handle_data(self, data: str):
        """Handle text content (for inline scripts, etc.)."""
        if self.current_tag == 'script' and not self.current_attrs.get('src'):
            # Inline script
            script_info = {
                'type': 'inline',
                'content': data.strip()[:500],  # Limit content size
                'attrs': self.current_attrs
            }
            self.scripts.append(script_info)


class HtmlExtractor:
    """Extracts frontend artifacts from HTML/HTM files."""
    
    def __init__(self):
        """Initialize the HTML extractor."""
        pass
    
    def extract_html_artifacts(self, html_files: List[str]) -> List[Dict[str, Any]]:
        """Extract artifacts from HTML/HTM files.
        
        Args:
            html_files: List of HTML/HTM file paths
            
        Returns:
            List of HTML artifact dictionaries
        """
        artifacts = []
        
        for html_file in html_files:
            try:
                artifact = self._extract_single_html_file(html_file)
                if artifact:
                    artifacts.append(artifact)
            except Exception as e:
                logger.error(f"Failed to extract HTML from {html_file}: {e}")
                continue
        
        logger.info(f"Extracted {len(artifacts)} HTML artifacts")
        return artifacts
    
    def _extract_single_html_file(self, html_file: str) -> Optional[Dict[str, Any]]:
        """Extract information from a single HTML/HTM file.
        
        Args:
            html_file: Path to HTML file
            
        Returns:
            Dictionary with extracted artifact information
        """
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Parse HTML
            parser = GwtHtmlParser()
            parser.feed(content)
            
            # Detect GWT features
            is_gwt = len(parser.gwt_modules) > 0 or len(parser.gwt_nocache) > 0
            gwt_indicators = []
            if parser.gwt_modules:
                gwt_indicators.append(f"GWT modules: {', '.join(parser.gwt_modules)}")
            if parser.gwt_nocache:
                gwt_indicators.append(f"GWT nocache scripts: {len(parser.gwt_nocache)}")
            
            # Check for GWT-related patterns in content
            gwt_patterns = [
                r'gwt\.nocache\.js',
                r'\.nocache\.js',
                r'com\.google\.gwt',
                r'gwt\.onLoad',
                r'__gwt_getMetaProperty',
                r'__MODULE_FUNC__'
            ]
            for pattern in gwt_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    is_gwt = True
                    gwt_indicators.append(f"Pattern match: {pattern}")
            
            # Extract title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1).strip() if title_match else ''
            title = unescape(re.sub(r'<[^>]+>', '', title))
            
            # Extract body content preview
            body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
            body_preview = body_match.group(1)[:500] if body_match else ''
            body_preview = unescape(re.sub(r'<[^>]+>', ' ', body_preview))
            
            # Build artifact text
            artifact_text_parts = [f"[HTML] {Path(html_file).name}"]
            if title:
                artifact_text_parts.append(f"Title: {title}")
            if is_gwt:
                artifact_text_parts.append("GWT-enabled")
            if parser.forms:
                artifact_text_parts.append(f"{len(parser.forms)} form(s)")
            if parser.scripts:
                artifact_text_parts.append(f"{len(parser.scripts)} script(s)")
            
            artifact_text = " | ".join(artifact_text_parts)
            
            # Create artifact
            artifact = {
                'project': extract_project_name_from_path(html_file),
                'path': html_file,
                'text': artifact_text,
                'title': title,
                'isGwt': str(is_gwt).lower(),  # Convert to string for Weaviate
                'gwt_modules': list(parser.gwt_modules),
                'gwt_nocache_scripts': list(parser.gwt_nocache),
                'gwt_indicators': gwt_indicators,
                'forms': parser.forms,
                'scripts': parser.scripts,
                'links': parser.links[:50],  # Limit links
                'meta_tags': parser.meta_tags,
                'body_preview': body_preview,
                'meta': {
                    'fileName': Path(html_file).name,
                    'fileSize': len(content),
                    'formCount': len(parser.forms),
                    'scriptCount': len(parser.scripts),
                    'linkCount': len(parser.links),
                    'hasGwt': is_gwt,
                    'gwtModules': list(parser.gwt_modules),
                    'gwtIndicators': gwt_indicators
                }
            }
            
            return artifact
            
        except Exception as e:
            logger.error(f"Failed to extract HTML from {html_file}: {e}")
            return None
    
    def _get_project_name(self, file_path: str) -> str:
        """Extract project name from file path."""
        return extract_project_name_from_path(file_path)
    
    def _save_artifacts(self, artifacts: List[Dict[str, Any]], output_dir: Path = None):
        """Save extracted artifacts to JSON file.
        
        Args:
            artifacts: List of artifact dictionaries
            output_dir: Output directory (defaults to settings.build_dir)
        """
        if output_dir is None:
            output_dir = settings.build_dir / 'html_artifacts'
        
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / 'all_html_artifacts.json'
        
        import json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(artifacts, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(artifacts)} HTML artifacts to {output_file}")

