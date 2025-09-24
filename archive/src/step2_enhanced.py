import asyncio
import os
import json
import logging
import re
import time
from pathlib import Path
from typing import Dict, Any, List, Set
from dotenv import load_dotenv
from logger_config import setup_logging
from ai_providers import create_ai_provider
from rate_limiter import RateLimiter, RateLimitConfig
from chromadb_connector import EnhancedChromaDBConnector
import uuid
from datetime import datetime

logger = logging.getLogger('java_analysis.step2_enhanced')

class EnhancedRequirementsProcessor:
    def __init__(self):
        load_dotenv()
        self.processed_files: Set[str] = set()
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        self.requirements_dir = Path(self.output_dir) / "requirements_enhanced"
        self.requirements_dir.mkdir(parents=True, exist_ok=True)
        
        # Enhanced metadata files
        self.enhanced_metadata_file = Path(self.output_dir) / "enhanced_metadata.json"
        self.architecture_report_file = Path(self.output_dir) / "enhanced_architecture_report.json"
        
        # StrictDoc configuration
        self.strictdoc_enabled = os.getenv('STRICTDOC', 'false').lower() == 'true'
        if self.strictdoc_enabled:
            self.strictdoc_dir = Path(self.output_dir) / "strictdoc_enhanced"
            self.strictdoc_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Enhanced StrictDoc generation enabled")
        
        # Initialize enhanced ChromaDB connector
        self.chromadb_connector = EnhancedChromaDBConnector()
        logger.info("Initialized enhanced ChromaDB connector with intelligent code chunking")
        
        # Enhanced rate limiting settings
        rate_config = RateLimitConfig(
            requests_per_minute=15,
            requests_per_hour=800,
            delay_between_requests=5.0,
            exponential_backoff_base=2.0,
            max_retries=5
        )
        self.rate_limiter = RateLimiter(rate_config)
        
        # Batch processing settings
        self.max_files_per_batch = 3
        self.max_files_to_process = 500000
        
        # Initialize AI provider
        self.ai_provider = create_ai_provider()
        logger.info(f"Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")
        
        # Load enhanced metadata
        self.enhanced_metadata = self.load_enhanced_metadata()
        self.architecture_report = self.load_architecture_report()

    def load_enhanced_metadata(self) -> Dict[str, Any]:
        """Load enhanced metadata from Step1_Enhanced"""
        try:
            if not self.enhanced_metadata_file.exists():
                logger.warning(f"Enhanced metadata file not found: {self.enhanced_metadata_file}")
                return {}
            
            with open(self.enhanced_metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            logger.info(f"Loaded enhanced metadata with {len(metadata)} entries")
            return metadata
            
        except Exception as e:
            logger.error(f"Error loading enhanced metadata: {e}")
            return {}

    def load_architecture_report(self) -> Dict[str, Any]:
        """Load architecture report from Step1_Enhanced"""
        try:
            if not self.architecture_report_file.exists():
                logger.warning(f"Architecture report file not found: {self.architecture_report_file}")
                return {}
            
            with open(self.architecture_report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            logger.info(f"Loaded architecture report with {len(report.get('layers', {}))} layers")
            return report
            
        except Exception as e:
            logger.error(f"Error loading architecture report: {e}")
            return {}

    def get_layer_directory(self, layer: str) -> Path:
        """Get directory for a specific architectural layer"""
        layer_dir = self.requirements_dir / layer.lower().replace(' ', '_')
        layer_dir.mkdir(parents=True, exist_ok=True)
        return layer_dir

    def get_component_directory(self, layer: str, component: str) -> Path:
        """Get directory for a specific component within a layer"""
        layer_dir = self.get_layer_directory(layer)
        component_dir = layer_dir / component.lower().replace(' ', '_')
        component_dir.mkdir(parents=True, exist_ok=True)
        return component_dir

    def get_unique_filename(self, base_dir: Path, filename: str, extension: str = '.md') -> Path:
        """Get unique filename with numbering if file exists"""
        base_name = filename
        counter = 0
        
        while True:
            if counter == 0:
                full_filename = f"{base_name}{extension}"
            else:
                full_filename = f"{base_name}-{counter}{extension}"
            
            file_path = base_dir / full_filename
            if not file_path.exists():
                return file_path
            
            counter += 1

    def convert_to_enhanced_strictdoc(self, markdown_content: str, file_path: str, 
                                     layer: str, component: str, classification: Dict[str, Any]) -> str:
        """Convert markdown content to enhanced StrictDoc format with architectural context"""
        # Extract title from markdown
        title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
        title = title_match.group(1) if title_match else f"Enhanced Requirements: {file_path}"
        
        # Remove the first heading line
        content_without_title = re.sub(r'^#\s+.+$', '', markdown_content, count=1, flags=re.MULTILINE).strip()
        
        # Generate a unique UID for the document
        uid = Path(file_path).stem.lower().replace('_', '-').replace('.', '-')
        
        # Parse the content to extract different sections
        sections = self._parse_content_sections(content_without_title)
        
        # Create enhanced StrictDoc with architectural metadata
        strictdoc_content = f"""[DOCUMENT]
TITLE: {title}
UID: REQ-ENHANCED-{uid.upper()}
CLASSIFICATION: {classification.get('primary_layer', 'Unknown')}
COMPONENT: {component}
LAYER: {layer}
PATTERN: {classification.get('pattern', 'Unknown')}
COMPLEXITY: {classification.get('complexity_score', 'Unknown')}

[REQUIREMENT]
UID: REQ-ARCH-INFO
TITLE: Architectural Information
STATEMENT: >>>
This component belongs to the {layer} layer and implements the {component} component.
Classification: {classification.get('primary_layer', 'Unknown')}
Pattern: {classification.get('pattern', 'Unknown')}
Complexity Score: {classification.get('complexity_score', 'Unknown')}
Technology: {classification.get('technology', 'Unknown')}
<<<
[/REQUIREMENT]

"""
        
        # Add requirements based on parsed sections
        req_counter = 1
        for section_name, section_content in sections.items():
            if section_content.strip():
                req_uid = f"REQ-{req_counter:03d}"
                
                # Clean up the content to avoid parsing issues
                clean_content = section_content.strip().replace('\n', ' ').replace('  ', ' ')
                if len(clean_content) > 150:
                    clean_content = clean_content[:150] + "..."
                
                strictdoc_content += f"""[REQUIREMENT]
UID: {req_uid}
TITLE: {section_name}
STATEMENT: >>>
{clean_content}
<<<
[/REQUIREMENT]

"""
                req_counter += 1
        
        strictdoc_content += "[/DOCUMENT]"
        return strictdoc_content

    def _parse_content_sections(self, content: str) -> dict:
        """Parse content into sections based on numbered lists and headers"""
        sections = {}
        
        # Split by numbered sections (1., 2., 3., etc.)
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # Check for numbered section headers
            section_match = re.match(r'^(\d+)\.\s+(.+)$', line.strip())
            if section_match:
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = section_match.group(2).strip()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # If no sections found, create a default one
        if not sections:
            sections["General Requirements"] = content
        
        return sections

    def prioritize_enhanced_files(self, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize files based on enhanced architectural classification"""
        prioritized_files = []
        
        # Group files by layer and component
        layer_groups = {}
        for file_path, file_data in metadata.items():
            if not isinstance(file_data, dict):
                continue
                
            classification = file_data.get('classification', {})
            layer = classification.get('primary_layer', 'Unknown')
            component = classification.get('component', 'Unknown')
            
            if layer not in layer_groups:
                layer_groups[layer] = {}
            if component not in layer_groups[layer]:
                layer_groups[layer][component] = []
            
            layer_groups[layer][component].append({
                'file_path': file_path,
                'file_data': file_data,
                'layer': layer,
                'component': component,
                'classification': classification
            })
        
        # Priority order for layers
        layer_priority = [
            'Presentation Layer',
            'Business Logic Layer',
            'Data Access Layer',
            'Integration Layer',
            'Configuration Layer',
            'Unknown'
        ]
        
        # Process files in layer priority order
        for layer in layer_priority:
            if layer in layer_groups:
                for component, files in layer_groups[layer].items():
                    # Sort files within component by complexity score
                    files.sort(key=lambda x: x['classification'].get('complexity_score', 0), reverse=True)
                    prioritized_files.extend(files)
                    
                    # Limit total files to process
                    if len(prioritized_files) >= self.max_files_to_process:
                        break
                        
            if len(prioritized_files) >= self.max_files_to_process:
                break
        
        return prioritized_files

    async def analyze_enhanced_files_batch(self, files_batch: List[Dict[str, Any]]) -> None:
        """Analyze multiple files in a single API call with enhanced architectural context"""
        if not files_batch:
            return
            
        logger.info(f"Analyzing enhanced batch of {len(files_batch)} files")
        
        # Wait for rate limiter before making API call
        await self.rate_limiter.wait_if_needed()
        
        # Create enhanced prompt with architectural context
        files_content = []
        for file_info in files_batch:
            file_path = file_info['file_path']
            file_data = file_info['file_data']
            layer = file_info['layer']
            component = file_info['component']
            classification = file_info['classification']
            
            # Get content preview
            content_preview = file_data.get('content', '')[:600]
            
            # Create enhanced file description
            file_description = f"""
File: {file_path}
Layer: {layer}
Component: {component}
Classification: {classification.get('primary_layer', 'Unknown')}
Pattern: {classification.get('pattern', 'Unknown')}
Technology: {classification.get('technology', 'Unknown')}
Complexity Score: {classification.get('complexity_score', 'Unknown')}

Content Preview:
{content_preview}
---"""
            files_content.append(file_description)
        
        combined_content = "\n".join(files_content)
        
        # Enhanced prompt with architectural awareness
        prompt = f"""Analyze the following files with their architectural context and provide enhanced requirements documentation:

{combined_content}

For each file, provide a comprehensive analysis considering its architectural layer and component classification:

1. **Architectural Purpose**: How this file fits into the overall system architecture
2. **Layer-Specific Functionality**: Functions specific to its architectural layer
3. **Component Interactions**: How it interacts with other components
4. **Business Requirements**: Business rules and logic implemented
5. **Data Flow**: Data handling and transformation
6. **Integration Points**: External system integrations
7. **Quality Attributes**: Performance, security, maintainability considerations
8. **Modernization Opportunities**: Potential improvements for cloud migration

Format your response as:
## File: [filename]
### Layer: [layer] | Component: [component]
[detailed analysis with the 8 sections above]

## File: [filename]
### Layer: [layer] | Component: [component]
[detailed analysis with the 8 sections above]
..."""
        
        for attempt in range(self.rate_limiter.config.max_retries):
            try:
                # Wait for rate limiter (includes exponential backoff for retries)
                if attempt > 0:
                    await self.rate_limiter.wait_if_needed()
                
                analysis = await self.ai_provider.create_chat_completion(
                    messages=[
                        {"role": "system", "content": "You are an expert software architect and requirements analyst. Provide comprehensive analysis considering architectural layers and modern software patterns."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=3000
                )
                
                # Record successful request
                self.rate_limiter.record_request()
                
                # Parse the response and create organized files
                await self.parse_enhanced_batch_response(analysis, files_batch)
                
                # Mark files as processed
                for file_info in files_batch:
                    self.processed_files.add(file_info['file_path'])
                
                logger.info(f"Successfully analyzed enhanced batch of {len(files_batch)} files")
                
                # Log rate limiting stats
                stats = self.rate_limiter.get_stats()
                logger.info(f"Rate limit stats: {stats['requests_last_minute']}/min, {stats['requests_last_hour']}/hour")
                
                break
                
            except Exception as e:
                logger.error(f"Error analyzing enhanced batch (attempt {attempt + 1}): {str(e)}")
                self.rate_limiter.record_failure()
                
                if attempt == self.rate_limiter.config.max_retries - 1:
                    logger.error(f"Failed to analyze enhanced batch after {self.rate_limiter.config.max_retries} attempts")
                    # Mark files as processed to avoid infinite retries
                    for file_info in files_batch:
                        self.processed_files.add(file_info['file_path'])

    async def parse_enhanced_batch_response(self, analysis: str, files_batch: List[Dict[str, Any]]) -> None:
        """Parse enhanced batch response and create organized documentation"""
        # Split by file sections
        sections = re.split(r'## File:\s*', analysis)
        
        for i, file_info in enumerate(files_batch):
            file_path = file_info['file_path']
            layer = file_info['layer']
            component = file_info['component']
            classification = file_info['classification']
            
            # Get component directory
            component_dir = self.get_component_directory(layer, component)
            
            # Get unique filename
            base_filename = Path(file_path).stem
            md_file_path = self.get_unique_filename(component_dir, base_filename, '.md')
            
            # Get the corresponding section content
            if i + 1 < len(sections):
                section_content = sections[i + 1].strip()
            else:
                section_content = "Enhanced analysis not available for this file."
            
            # Create enhanced markdown content with metadata
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            markdown_content = f"""# Enhanced Requirements Analysis: {file_path}

**Generated**: {timestamp}  
**Layer**: {layer}  
**Component**: {component}  
**Classification**: {classification.get('primary_layer', 'Unknown')}  
**Pattern**: {classification.get('pattern', 'Unknown')}  
**Technology**: {classification.get('technology', 'Unknown')}  
**Complexity Score**: {classification.get('complexity_score', 'Unknown')}

## Architectural Context

This file is part of the **{layer}** layer and implements the **{component}** component. It has been classified with a complexity score of {classification.get('complexity_score', 'Unknown')} and follows the {classification.get('pattern', 'Unknown')} pattern.

## Detailed Analysis

{section_content}

## Metadata

```json
{json.dumps(classification, indent=2)}
```
"""
            
            # Write enhanced markdown file
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.debug(f"Generated enhanced requirements document: {md_file_path}")
            
            # Generate enhanced StrictDoc version if enabled
            if self.strictdoc_enabled:
                strictdoc_component_dir = self.strictdoc_dir / layer.lower().replace(' ', '_') / component.lower().replace(' ', '_')
                strictdoc_component_dir.mkdir(parents=True, exist_ok=True)
                
                strictdoc_file_path = self.get_unique_filename(strictdoc_component_dir, base_filename, '.sdoc')
                strictdoc_content = self.convert_to_enhanced_strictdoc(markdown_content, file_path, layer, component, classification)
                
                with open(strictdoc_file_path, 'w', encoding='utf-8') as f:
                    f.write(strictdoc_content)
                
                logger.debug(f"Generated enhanced StrictDoc document: {strictdoc_file_path}")

    async def process_enhanced_files_with_batching(self) -> None:
        """Process enhanced files in batches with architectural organization"""
        if not self.enhanced_metadata:
            logger.error("No enhanced metadata available. Please run Step1_Enhanced.sh first.")
            return
        
        prioritized_files = self.prioritize_enhanced_files(self.enhanced_metadata)
        
        logger.info(f"Processing {len(prioritized_files)} enhanced files in batches of {self.max_files_per_batch}")
        
        # Process files in batches
        for i in range(0, len(prioritized_files), self.max_files_per_batch):
            batch = prioritized_files[i:i + self.max_files_per_batch]
            await self.analyze_enhanced_files_batch(batch)
            
            # Progress update
            processed_count = len(self.processed_files)
            total_count = len(prioritized_files)
            logger.info(f"Enhanced progress: {processed_count}/{total_count} files processed")

    def generate_enhanced_index(self) -> None:
        """Generate enhanced index with architectural organization"""
        index_path = self.requirements_dir / "step2_enhanced_index.md"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# Enhanced Requirements Documentation Index\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total files processed**: {len(self.processed_files)}\n\n")
            
            # Architecture overview
            if self.architecture_report:
                f.write("## Architecture Overview\n\n")
                layers = self.architecture_report.get('layers', {})
                for layer, layer_info in layers.items():
                    f.write(f"### {layer}\n")
                    f.write(f"- **Files**: {layer_info.get('file_count', 0)}\n")
                    f.write(f"- **Components**: {len(layer_info.get('components', []))}\n")
                    f.write(f"- **Technologies**: {', '.join(layer_info.get('technologies', []))}\n\n")
            
            f.write("## Enhanced Requirements Documents by Layer and Component\n\n")
            
            # Group files by layer and component
            layer_structure = {}
            for file_path in sorted(self.processed_files):
                # Find file in enhanced metadata
                file_data = self.enhanced_metadata.get(file_path, {})
                classification = file_data.get('classification', {})
                layer = classification.get('primary_layer', 'Unknown')
                component = classification.get('component', 'Unknown')
                
                if layer not in layer_structure:
                    layer_structure[layer] = {}
                if component not in layer_structure[layer]:
                    layer_structure[layer][component] = []
                
                layer_structure[layer][component].append(file_path)
            
            # Write organized index
            for layer in sorted(layer_structure.keys()):
                f.write(f"### {layer}\n\n")
                for component in sorted(layer_structure[layer].keys()):
                    f.write(f"#### {component}\n\n")
                    for file_path in layer_structure[layer][component]:
                        md_filename = f"{Path(file_path).stem}.md"
                        relative_path = f"{layer.lower().replace(' ', '_')}/{component.lower().replace(' ', '_')}/{md_filename}"
                        f.write(f"- [{file_path}](./{relative_path})\n")
                    f.write("\n")
        
        logger.info(f"Generated enhanced index file: {index_path}")
        
        # Generate enhanced StrictDoc index if enabled
        if self.strictdoc_enabled:
            self.generate_strictdoc_index(layer_structure)

    def generate_strictdoc_index(self, layer_structure: Dict[str, Dict[str, List[str]]]) -> None:
        """Generate enhanced StrictDoc index"""
        strictdoc_index_path = self.strictdoc_dir / "step2_enhanced_strictdoc_index.md"
        
        with open(strictdoc_index_path, 'w', encoding='utf-8') as f:
            f.write("# Enhanced StrictDoc Documentation Index\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total files processed**: {len(self.processed_files)}\n\n")
            f.write("## Enhanced StrictDoc Documents by Layer and Component\n\n")
            
            # Write organized StrictDoc index
            for layer in sorted(layer_structure.keys()):
                f.write(f"### {layer}\n\n")
                for component in sorted(layer_structure[layer].keys()):
                    f.write(f"#### {component}\n\n")
                    for file_path in layer_structure[layer][component]:
                        sdoc_filename = f"{Path(file_path).stem}.sdoc"
                        relative_path = f"{layer.lower().replace(' ', '_')}/{component.lower().replace(' ', '_')}/{sdoc_filename}"
                        f.write(f"- [{file_path}](./{relative_path})\n")
                    f.write("\n")
        
        logger.info(f"Generated enhanced StrictDoc index file: {strictdoc_index_path}")

async def generate_enhanced_requirements():
    """Main function to generate enhanced requirements documentation"""
    logger = setup_logging(level=logging.INFO)
    logger.info("Starting enhanced requirements generation process")
    
    try:
        processor = EnhancedRequirementsProcessor()
        
        # Process enhanced files with batching
        await processor.process_enhanced_files_with_batching()
        
        # Generate enhanced index
        processor.generate_enhanced_index()
        
        logger.info("Enhanced requirements generation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during enhanced requirements generation: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(generate_enhanced_requirements())