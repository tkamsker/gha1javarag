"""
Chunking and embedding system for all artifact types.
"""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
import numpy as np

from config.settings import settings

logger = logging.getLogger(__name__)

class ChunkBuilder:
    """Builds chunks and embeddings for all artifact types."""
    
    def __init__(self):
        """Initialize chunk builder."""
        self.output_dir = settings.build_dir / "chunks"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ollama API endpoints
        self.ollama_embed_url = f"{settings.ollama_base_url}/api/embeddings"
        self.ollama_generate_url = f"{settings.ollama_base_url}/api/generate"
    
    def build_chunks_for_artifacts(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Build chunks for all artifact types."""
        all_chunks = []
        
        # Process each artifact type
        for artifact_type, artifact_list in artifacts.items():
            logger.info(f"Building chunks for {artifact_type}: {len(artifact_list)} artifacts")
            
            for artifact in artifact_list:
                chunks = self._build_chunks_for_artifact(artifact, artifact_type)
                all_chunks.extend(chunks)
        
        # Save all chunks
        self._save_all_chunks_json(all_chunks)
        
        logger.info(f"Built {len(all_chunks)} chunks total")
        return all_chunks
    
    def _build_chunks_for_artifact(self, artifact: Dict[str, Any], artifact_type: str) -> List[Dict[str, Any]]:
        """Build chunks for a single artifact."""
        chunks = []
        
        # Create header chunk
        header_chunk = self._create_header_chunk(artifact, artifact_type)
        if header_chunk:
            chunks.append(header_chunk)
        
        # Create content chunks
        content_chunks = self._create_content_chunks(artifact, artifact_type)
        chunks.extend(content_chunks)
        
        # Generate embeddings for all chunks
        for chunk in chunks:
            chunk['embedding'] = self._generate_embedding(chunk['text'])
        
        return chunks
    
    def _create_header_chunk(self, artifact: Dict[str, Any], artifact_type: str) -> Optional[Dict[str, Any]]:
        """Create a header chunk for the artifact."""
        try:
            header_text = self._generate_header_text(artifact, artifact_type)
            
            if not header_text:
                return None
            
            chunk = {
                'project': artifact.get('project', 'unknown'),
                'path': artifact.get('path', ''),
                'lineStart': artifact.get('lineStart', 1),
                'lineEnd': artifact.get('lineEnd', 1),
                'text': header_text,
                'meta': {
                    'chunkType': 'header',
                    'artifactType': artifact_type,
                    'originalArtifact': artifact.get('meta', {})
                },
                'embedding': None  # Will be filled later
            }
            
            return chunk
            
        except Exception as e:
            logger.error(f"Failed to create header chunk: {e}")
            return None
    
    def _create_content_chunks(self, artifact: Dict[str, Any], artifact_type: str) -> List[Dict[str, Any]]:
        """Create content chunks for the artifact."""
        chunks = []
        
        try:
            # Extract content based on artifact type
            content_parts = self._extract_content_parts(artifact, artifact_type)
            
            for i, content_part in enumerate(content_parts):
                if content_part and content_part.strip():
                    chunk = {
                        'project': artifact.get('project', 'unknown'),
                        'path': artifact.get('path', ''),
                        'lineStart': artifact.get('lineStart', 1),
                        'lineEnd': artifact.get('lineEnd', 1),
                        'text': content_part,
                        'meta': {
                            'chunkType': 'content',
                            'artifactType': artifact_type,
                            'contentIndex': i,
                            'originalArtifact': artifact.get('meta', {})
                        },
                        'embedding': None  # Will be filled later
                    }
                    chunks.append(chunk)
            
        except Exception as e:
            logger.error(f"Failed to create content chunks: {e}")
        
        return chunks
    
    def _generate_header_text(self, artifact: Dict[str, Any], artifact_type: str) -> str:
        """Generate header text for the artifact."""
        if artifact_type == 'gwt_modules':
            return self._generate_gwt_module_header(artifact)
        elif artifact_type == 'gwt_activities_places':
            return self._generate_gwt_activity_place_header(artifact)
        elif artifact_type == 'gwt_uibinder':
            return self._generate_gwt_uibinder_header(artifact)
        elif artifact_type == 'gwt_endpoints':
            return self._generate_gwt_endpoint_header(artifact)
        elif artifact_type == 'js_artifacts':
            return self._generate_js_artifact_header(artifact)
        elif artifact_type == 'ibatis_statements':
            return self._generate_ibatis_statement_header(artifact)
        elif artifact_type == 'dao_calls':
            return self._generate_dao_call_header(artifact)
        elif artifact_type == 'jsp_forms':
            return self._generate_jsp_form_header(artifact)
        elif artifact_type == 'db_tables':
            return self._generate_db_table_header(artifact)
        else:
            return f"[{artifact_type.upper()}] {artifact.get('text', 'Unknown artifact')}"
    
    def _generate_gwt_module_header(self, artifact: Dict[str, Any]) -> str:
        """Generate GWT module header."""
        module_name = artifact.get('moduleName', 'Unknown')
        entry_points = artifact.get('entryPoints', [])
        inherits = artifact.get('inherits', [])
        
        header = f"[GWT Module] {module_name}"
        if entry_points:
            header += f" (entryPoints={len(entry_points)})"
        
        if inherits:
            header += f"\ninherits: {', '.join(inherits[:3])}"
            if len(inherits) > 3:
                header += f" (+{len(inherits) - 3} more)"
        
        return header
    
    def _generate_gwt_activity_place_header(self, artifact: Dict[str, Any]) -> str:
        """Generate GWT Activity/Place header."""
        place_class = artifact.get('placeClass', 'Unknown')
        activity_class = artifact.get('activityClass', 'Unknown')
        place_token = artifact.get('placeToken', '')
        
        if activity_class and activity_class != 'Unknown':
            header = f"[GWT Place/Activity] {place_class} ↔ {activity_class}"
        else:
            header = f"[GWT Place] {place_class}"
        
        if place_token:
            header += f"\ntoken: {place_token}"
        
        navigates_to = artifact.get('navigatesTo', [])
        if navigates_to:
            header += f"\nnavigatesTo: {', '.join(navigates_to[:2])}"
            if len(navigates_to) > 2:
                header += f" (+{len(navigates_to) - 2} more)"
        
        calls_services = artifact.get('callsServices', [])
        if calls_services:
            header += f"\ncallsServices: {', '.join(calls_services[:2])}"
            if len(calls_services) > 2:
                header += f" (+{len(calls_services) - 2} more)"
        
        return header
    
    def _generate_gwt_uibinder_header(self, artifact: Dict[str, Any]) -> str:
        """Generate GWT UiBinder header."""
        ui_xml_path = artifact.get('uiXmlPath', 'Unknown')
        owner_type = artifact.get('ownerType', 'Unknown')
        
        header = f"[UiBinder] {Path(ui_xml_path).name} (owner={owner_type})"
        
        # Parse widgets JSON
        try:
            widgets_json = artifact.get('widgetsJson', '[]')
            widgets = json.loads(widgets_json) if isinstance(widgets_json, str) else widgets_json
            if widgets:
                widget_summary = ', '.join([f"{w.get('fieldName', '')}:{w.get('widgetType', '')}" for w in widgets[:3]])
                header += f"\nwidgets: {widget_summary}"
                if len(widgets) > 3:
                    header += f" (+{len(widgets) - 3} more)"
        except:
            pass
        
        # Parse events JSON
        try:
            events_json = artifact.get('eventsJson', '[]')
            events = json.loads(events_json) if isinstance(events_json, str) else events_json
            if events:
                event_summary = ', '.join([f"{e.get('fieldName', '')}.{e.get('eventType', '')}" for e in events[:2]])
                header += f"\nevents: {event_summary}"
                if len(events) > 2:
                    header += f" (+{len(events) - 2} more)"
        except:
            pass
        
        i18n_keys = artifact.get('i18nKeys', [])
        if i18n_keys:
            header += f"\ni18n: {', '.join(i18n_keys[:2])}"
            if len(i18n_keys) > 2:
                header += f" (+{len(i18n_keys) - 2} more)"
        
        return header
    
    def _generate_gwt_endpoint_header(self, artifact: Dict[str, Any]) -> str:
        """Generate GWT endpoint header."""
        style = artifact.get('style', 'Unknown')
        service_interface = artifact.get('serviceInterface', 'Unknown')
        endpoint_path = artifact.get('endpointPath', '')
        
        header = f"[GWT {style}] {service_interface}"
        if endpoint_path:
            header += f" @ {endpoint_path}"
        
        # Parse methods JSON
        try:
            methods_json = artifact.get('methodsJson', '[]')
            methods = json.loads(methods_json) if isinstance(methods_json, str) else methods_json
            if methods:
                method_names = [m.get('name', '') for m in methods[:3]]
                header += f"\nmethods: {', '.join(method_names)}"
                if len(methods) > 3:
                    header += f" (+{len(methods) - 3} more)"
        except:
            pass
        
        server_impl = artifact.get('serverImpl', '')
        if server_impl:
            header += f"\nserverImpl: {server_impl}"
        
        return header
    
    def _generate_js_artifact_header(self, artifact: Dict[str, Any]) -> str:
        """Generate JavaScript artifact header."""
        script_path = artifact.get('scriptPath', 'Unknown')
        
        header = f"[JS] {Path(script_path).name}"
        
        # Parse routes JSON
        try:
            routes_json = artifact.get('routesJson', '[]')
            routes = json.loads(routes_json) if isinstance(routes_json, str) else routes_json
            if routes:
                route_patterns = [r.get('pattern', '') for r in routes[:2]]
                header += f"\nroutes: {', '.join(route_patterns)}"
                if len(routes) > 2:
                    header += f" (+{len(routes) - 2} more)"
        except:
            pass
        
        # Parse XHR JSON
        try:
            xhr_json = artifact.get('xhrJson', '[]')
            xhr_calls = json.loads(xhr_json) if isinstance(xhr_json, str) else xhr_json
            if xhr_calls:
                xhr_summary = ', '.join([f"{x.get('method', '')} {x.get('url', '')}" for x in xhr_calls[:2]])
                header += f"\nxhr: {xhr_summary}"
                if len(xhr_calls) > 2:
                    header += f" (+{len(xhr_calls) - 2} more)"
        except:
            pass
        
        # Parse validations JSON
        try:
            validations_json = artifact.get('validationsJson', '[]')
            validations = json.loads(validations_json) if isinstance(validations_json, str) else validations_json
            if validations:
                validation_rules = [str(v.get('rule', '')) for v in validations[:2]]
                header += f"\nvalidations: {', '.join(validation_rules)}"
                if len(validations) > 2:
                    header += f" (+{len(validations) - 2} more)"
        except:
            pass
        
        return header
    
    def _generate_ibatis_statement_header(self, artifact: Dict[str, Any]) -> str:
        """Generate iBATIS statement header."""
        statement_id = artifact.get('statementId', 'Unknown')
        statement_type = artifact.get('statementType', 'Unknown')
        
        header = f"[iBATIS {statement_type}] {statement_id}"
        
        sql_content = artifact.get('sqlContent', '')
        if sql_content:
            # Truncate SQL content for header
            sql_preview = sql_content[:100].replace('\n', ' ').strip()
            if len(sql_content) > 100:
                sql_preview += "..."
            header += f"\nSQL: {sql_preview}"
        
        return header
    
    def _generate_dao_call_header(self, artifact: Dict[str, Any]) -> str:
        """Generate DAO call header."""
        dao_class = artifact.get('daoClass', 'Unknown')
        method_name = artifact.get('methodName', 'Unknown')
        
        header = f"[DAO Call] {dao_class}.{method_name}"
        
        statement_refs = artifact.get('statementRefs', [])
        if statement_refs:
            header += f"\nstatements: {', '.join(statement_refs[:2])}"
            if len(statement_refs) > 2:
                header += f" (+{len(statement_refs) - 2} more)"
        
        return header
    
    def _generate_jsp_form_header(self, artifact: Dict[str, Any]) -> str:
        """Generate JSP form header."""
        form_action = artifact.get('formAction', 'Unknown')
        form_method = artifact.get('formMethod', 'GET')
        
        header = f"[JSP Form] {form_action} ({form_method})"
        
        fields = artifact.get('fields', [])
        if fields:
            field_summary = ', '.join([f.get('name', '') for f in fields[:3]])
            header += f"\nfields: {field_summary}"
            if len(fields) > 3:
                header += f" (+{len(fields) - 3} more)"
        
        return header
    
    def _generate_db_table_header(self, artifact: Dict[str, Any]) -> str:
        """Generate database table header."""
        table_name = artifact.get('tableName', 'Unknown')
        
        header = f"[DB Table] {table_name}"
        
        columns = artifact.get('columns', [])
        if columns:
            column_summary = ', '.join([c.get('name', '') for c in columns[:3]])
            header += f"\ncolumns: {column_summary}"
            if len(columns) > 3:
                header += f" (+{len(columns) - 3} more)"
        
        return header
    
    def _extract_content_parts(self, artifact: Dict[str, Any], artifact_type: str) -> List[str]:
        """Extract content parts for chunking."""
        content_parts = []
        
        # Get the main text content
        main_text = artifact.get('text', '')
        if main_text:
            content_parts.append(main_text)
        
        # Add artifact-specific content
        if artifact_type == 'gwt_modules':
            raw_xml = artifact.get('rawXml', '')
            if raw_xml:
                content_parts.append(f"XML Content:\n{raw_xml}")
        
        elif artifact_type == 'gwt_uibinder':
            widgets_json = artifact.get('widgetsJson', '')
            events_json = artifact.get('eventsJson', '')
            if widgets_json:
                content_parts.append(f"Widgets: {widgets_json}")
            if events_json:
                content_parts.append(f"Events: {events_json}")
        
        elif artifact_type == 'gwt_endpoints':
            methods_json = artifact.get('methodsJson', '')
            if methods_json:
                content_parts.append(f"Methods: {methods_json}")
        
        elif artifact_type == 'js_artifacts':
            routes_json = artifact.get('routesJson', '')
            xhr_json = artifact.get('xhrJson', '')
            validations_json = artifact.get('validationsJson', '')
            if routes_json:
                content_parts.append(f"Routes: {routes_json}")
            if xhr_json:
                content_parts.append(f"XHR Calls: {xhr_json}")
            if validations_json:
                content_parts.append(f"Validations: {validations_json}")
        
        elif artifact_type == 'ibatis_statements':
            sql_content = artifact.get('sqlContent', '')
            if sql_content:
                content_parts.append(f"SQL: {sql_content}")
        
        elif artifact_type == 'jsp_forms':
            fields = artifact.get('fields', [])
            validations = artifact.get('validations', [])
            if fields:
                content_parts.append(f"Fields: {json.dumps(fields, indent=2)}")
            if validations:
                content_parts.append(f"Validations: {json.dumps(validations, indent=2)}")
        
        elif artifact_type == 'db_tables':
            columns = artifact.get('columns', [])
            constraints = artifact.get('constraints', [])
            if columns:
                content_parts.append(f"Columns: {json.dumps(columns, indent=2)}")
            if constraints:
                content_parts.append(f"Constraints: {json.dumps(constraints, indent=2)}")
        
        return content_parts
    
    def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text using Ollama."""
        try:
            payload = {
                "model": settings.ollama_embed_model_name,
                "prompt": text
            }
            
            response = requests.post(
                self.ollama_embed_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('embedding', [])
            else:
                logger.error(f"Failed to generate embedding: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return None
    
    def _save_all_chunks_json(self, chunks: List[Dict[str, Any]]):
        """Save all chunks as JSON files."""
        # Save individual chunk files
        for i, chunk in enumerate(chunks):
            chunk_file = self.output_dir / f"chunk_{i:04d}.json"
            with open(chunk_file, 'w', encoding='utf-8') as f:
                json.dump(chunk, f, indent=2, ensure_ascii=False)
        
        # Save all chunks together
        all_chunks_file = self.output_dir / "all_chunks.json"
        with open(all_chunks_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(chunks)} chunks to {self.output_dir}")
