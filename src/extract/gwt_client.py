"""
GWT client code extraction for Activities, Places, RPC, and RequestFactory.
"""
import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import javalang
from javalang.tree import ClassDeclaration, MethodDeclaration, InterfaceDeclaration
from javalang.parser import JavaSyntaxError

from config.settings import settings

logger = logging.getLogger(__name__)

class GwtClientExtractor:
    """Extracts GWT client-side code patterns."""
    
    def __init__(self):
        """Initialize GWT client extractor."""
        self.output_dir = settings.build_dir / "gwt_client"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # GWT-specific patterns
        self.entry_point_interface = "com.google.gwt.core.client.EntryPoint"
        self.activity_interface = "com.google.gwt.activity.shared.Activity"
        self.place_class = "com.google.gwt.place.shared.Place"
        self.remote_service_interface = "com.google.gwt.user.client.rpc.RemoteService"
        self.request_factory_interface = "com.google.gwt.requestfactory.shared.RequestFactory"
    
    def extract_client_artifacts(self, java_files: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Extract GWT client artifacts from Java files."""
        artifacts = {
            'activities_places': [],
            'endpoints': [],
            'routes': []
        }
        
        # Filter for GWT client files
        gwt_client_files = [f for f in java_files if self._is_gwt_client_file(f)]
        
        for java_file in gwt_client_files:
            try:
                logger.info(f"Processing GWT client file: {java_file}")
                
                # Parse Java file
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = javalang.parse.parse(content)
                
                # Extract activities and places
                activities_places = self._extract_activities_places(tree, java_file)
                artifacts['activities_places'].extend(activities_places)
                
                # Extract RPC endpoints
                rpc_endpoints = self._extract_rpc_endpoints(tree, java_file)
                artifacts['endpoints'].extend(rpc_endpoints)
                
                # Extract RequestFactory endpoints
                rf_endpoints = self._extract_request_factory_endpoints(tree, java_file)
                artifacts['endpoints'].extend(rf_endpoints)
                
            except JavaSyntaxError as e:
                logger.warning(f"Java syntax error in {java_file}: {e}")
                continue
            except Exception as e:
                logger.error(f"Failed to process GWT client file {java_file}: {e}")
                continue
        
        # Save artifacts
        self._save_artifacts(artifacts)
        
        logger.info(f"Extracted {len(artifacts['activities_places'])} activities/places, "
                   f"{len(artifacts['endpoints'])} endpoints")
        
        return artifacts
    
    def _is_gwt_client_file(self, file_path: str) -> bool:
        """Check if file is likely a GWT client file."""
        path_lower = file_path.lower()
        return ('client' in path_lower or 
                'shared' in path_lower or
                'gwt' in path_lower)
    
    def _extract_activities_places(self, tree, file_path: str) -> List[Dict[str, Any]]:
        """Extract Activity/Place patterns."""
        activities_places = []
        
        for path, node in tree:
            if isinstance(node, ClassDeclaration):
                class_info = self._analyze_class_for_activity_place(node, file_path)
                if class_info:
                    activities_places.append(class_info)
        
        return activities_places
    
    def _analyze_class_for_activity_place(self, class_decl: ClassDeclaration, file_path: str) -> Optional[Dict[str, Any]]:
        """Analyze a class for Activity/Place patterns."""
        class_name = class_decl.name
        package_name = self._get_package_name(class_decl)
        full_class_name = f"{package_name}.{class_name}" if package_name else class_name
        
        # Check if it's an EntryPoint
        if self._implements_interface(class_decl, self.entry_point_interface):
            return self._create_entry_point_artifact(class_decl, file_path, full_class_name)
        
        # Check if it's an Activity
        if self._implements_interface(class_decl, self.activity_interface):
            return self._create_activity_artifact(class_decl, file_path, full_class_name)
        
        # Check if it's a Place
        if self._extends_class(class_decl, self.place_class):
            return self._create_place_artifact(class_decl, file_path, full_class_name)
        
        return None
    
    def _create_entry_point_artifact(self, class_decl: ClassDeclaration, file_path: str, full_class_name: str) -> Dict[str, Any]:
        """Create EntryPoint artifact."""
        return {
            'project': self._get_project_name(file_path),
            'path': file_path,
            'lineStart': class_decl.position.line if class_decl.position else 1,
            'lineEnd': class_decl.position.line + 50 if class_decl.position else 50,
            'text': f"[GWT EntryPoint] {full_class_name}",
            'meta': {
                'type': 'EntryPoint',
                'className': full_class_name
            },
            'placeClass': full_class_name,
            'activityClass': None,
            'placeToken': None,
            'views': [],
            'navigatesTo': [],
            'callsServices': []
        }
    
    def _create_activity_artifact(self, class_decl: ClassDeclaration, file_path: str, full_class_name: str) -> Dict[str, Any]:
        """Create Activity artifact."""
        # Try to find associated Place
        place_class = self._find_associated_place(class_decl)
        
        return {
            'project': self._get_project_name(file_path),
            'path': file_path,
            'lineStart': class_decl.position.line if class_decl.position else 1,
            'lineEnd': class_decl.position.line + 50 if class_decl.position else 50,
            'text': f"[GWT Activity] {full_class_name}",
            'meta': {
                'type': 'Activity',
                'className': full_class_name,
                'associatedPlace': place_class
            },
            'placeClass': place_class,
            'activityClass': full_class_name,
            'placeToken': self._extract_place_token(class_decl),
            'views': self._extract_view_references(class_decl),
            'navigatesTo': [],
            'callsServices': self._extract_service_calls(class_decl)
        }
    
    def _create_place_artifact(self, class_decl: ClassDeclaration, file_path: str, full_class_name: str) -> Dict[str, Any]:
        """Create Place artifact."""
        return {
            'project': self._get_project_name(file_path),
            'path': file_path,
            'lineStart': class_decl.position.line if class_decl.position else 1,
            'lineEnd': class_decl.position.line + 50 if class_decl.position else 50,
            'text': f"[GWT Place] {full_class_name}",
            'meta': {
                'type': 'Place',
                'className': full_class_name
            },
            'placeClass': full_class_name,
            'activityClass': None,
            'placeToken': self._extract_place_token(class_decl),
            'views': [],
            'navigatesTo': [],
            'callsServices': []
        }
    
    def _extract_rpc_endpoints(self, tree, file_path: str) -> List[Dict[str, Any]]:
        """Extract RPC service endpoints."""
        endpoints = []
        
        for path, node in tree:
            if isinstance(node, InterfaceDeclaration):
                if self._implements_interface(node, self.remote_service_interface):
                    endpoint = self._create_rpc_endpoint(node, file_path)
                    if endpoint:
                        endpoints.append(endpoint)
        
        return endpoints
    
    def _extract_request_factory_endpoints(self, tree, file_path: str) -> List[Dict[str, Any]]:
        """Extract RequestFactory endpoints."""
        endpoints = []
        
        for path, node in tree:
            if isinstance(node, InterfaceDeclaration):
                if self._implements_interface(node, self.request_factory_interface):
                    endpoint = self._create_request_factory_endpoint(node, file_path)
                    if endpoint:
                        endpoints.append(endpoint)
        
        return endpoints
    
    def _create_rpc_endpoint(self, interface_decl: InterfaceDeclaration, file_path: str) -> Optional[Dict[str, Any]]:
        """Create RPC endpoint artifact."""
        interface_name = interface_decl.name
        package_name = self._get_package_name(interface_decl)
        full_interface_name = f"{package_name}.{interface_name}" if package_name else interface_name
        
        # Extract methods
        methods = []
        for method in interface_decl.methods:
            if isinstance(method, MethodDeclaration):
                method_info = {
                    'name': method.name,
                    'parameters': [param.type.name for param in method.parameters] if method.parameters else [],
                    'returnType': method.return_type.name if method.return_type else 'void'
                }
                methods.append(method_info)
        
        return {
            'project': self._get_project_name(file_path),
            'path': file_path,
            'lineStart': interface_decl.position.line if interface_decl.position else 1,
            'lineEnd': interface_decl.position.line + 50 if interface_decl.position else 50,
            'text': f"[GWT RPC] {full_interface_name}",
            'meta': {
                'type': 'RPC',
                'interfaceName': full_interface_name
            },
            'style': 'RPC',
            'serviceInterface': full_interface_name,
            'asyncInterface': f"{full_interface_name}Async",
            'endpointPath': settings.gwt_rpc_default_path,
            'methodsJson': json.dumps(methods),
            'serverImpl': f"{full_interface_name}Impl"
        }
    
    def _create_request_factory_endpoint(self, interface_decl: InterfaceDeclaration, file_path: str) -> Optional[Dict[str, Any]]:
        """Create RequestFactory endpoint artifact."""
        interface_name = interface_decl.name
        package_name = self._get_package_name(interface_decl)
        full_interface_name = f"{package_name}.{interface_name}" if package_name else interface_name
        
        # Extract methods
        methods = []
        for method in interface_decl.methods:
            if isinstance(method, MethodDeclaration):
                method_info = {
                    'name': method.name,
                    'parameters': [param.type.name for param in method.parameters] if method.parameters else [],
                    'returnType': method.return_type.name if method.return_type else 'void'
                }
                methods.append(method_info)
        
        return {
            'project': self._get_project_name(file_path),
            'path': file_path,
            'lineStart': interface_decl.position.line if interface_decl.position else 1,
            'lineEnd': interface_decl.position.line + 50 if interface_decl.position else 50,
            'text': f"[GWT RequestFactory] {full_interface_name}",
            'meta': {
                'type': 'RequestFactory',
                'interfaceName': full_interface_name
            },
            'style': 'RequestFactory',
            'serviceInterface': full_interface_name,
            'asyncInterface': None,
            'endpointPath': settings.gwt_rf_default_path,
            'methodsJson': json.dumps(methods),
            'serverImpl': f"{full_interface_name}Impl"
        }
    
    def _implements_interface(self, class_decl, interface_name: str) -> bool:
        """Check if class implements the given interface."""
        if not hasattr(class_decl, 'implements') or not class_decl.implements:
            return False
        
        for impl in class_decl.implements:
            if hasattr(impl, 'name') and interface_name in impl.name:
                return True
        return False
    
    def _extends_class(self, class_decl, class_name: str) -> bool:
        """Check if class extends the given class."""
        if not hasattr(class_decl, 'extends') or not class_decl.extends:
            return False
        
        if hasattr(class_decl.extends, 'name'):
            return class_name in class_decl.extends.name
        return False
    
    def _get_package_name(self, class_decl) -> str:
        """Extract package name from class declaration."""
        # This is a simplified version - in practice, you'd need to traverse up the AST
        return "com.example.gwt.client"  # Placeholder
    
    def _get_project_name(self, file_path: str) -> str:
        """Extract project name from file path."""
        path_parts = Path(file_path).parts
        
        for part in path_parts:
            if part in ['src', 'main', 'java', 'webapp', 'resources', 'client', 'shared']:
                continue
            if '.' in part and len(part) > 3:
                return part.split('.')[0]
            if part and not part.startswith('.') and len(part) > 2:
                return part
        
        return settings.default_project_name
    
    def _find_associated_place(self, class_decl: ClassDeclaration) -> Optional[str]:
        """Find associated Place class for an Activity."""
        # This would require more sophisticated analysis
        return None
    
    def _extract_place_token(self, class_decl: ClassDeclaration) -> Optional[str]:
        """Extract place token pattern."""
        # This would require analyzing the class for token patterns
        return None
    
    def _extract_view_references(self, class_decl: ClassDeclaration) -> List[str]:
        """Extract view class references."""
        # This would require analyzing field declarations and method calls
        return []
    
    def _extract_service_calls(self, class_decl: ClassDeclaration) -> List[str]:
        """Extract service calls from the class."""
        # This would require analyzing method calls
        return []
    
    def _save_artifacts(self, artifacts: Dict[str, List[Dict[str, Any]]]):
        """Save extracted artifacts to JSON files."""
        for artifact_type, artifact_list in artifacts.items():
            output_file = self.output_dir / f"{artifact_type}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(artifact_list, f, indent=2, ensure_ascii=False)
        
        # Save all artifacts together
        all_artifacts_file = self.output_dir / "all_artifacts.json"
        with open(all_artifacts_file, 'w', encoding='utf-8') as f:
            json.dump(artifacts, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved GWT client artifacts to {self.output_dir}")
