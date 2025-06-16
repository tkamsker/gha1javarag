from chromadb_connector import ChromaDBConnector
from doxygen_parser import DoxygenParser
import logging
from typing import Dict, List
import json
import uuid

class ASTProcessor:
    def __init__(self, xml_dir: str):
        self.xml_dir = xml_dir
        self.logger = logging.getLogger(__name__)
        self.parser = DoxygenParser(xml_dir)
        self.db_connector = ChromaDBConnector()
        
    def process_and_store(self):
        """Process AST data and store it in ChromaDB"""
        try:
            # Get AST data from doxygen XML
            ast_data = self.parser.get_ast_data()
            
            # Prepare documents for storage
            documents = []
            metadatas = []
            ids = []
            
            # Process classes
            for class_info in ast_data.get('classes', []):
                try:
                    class_name = class_info.get('name')
                    if not class_name:
                        self.logger.warning("Skipping class with no name")
                        continue
                        
                    # Create a document for the class
                    class_doc = self._create_class_document(class_info)
                    documents.append(class_doc)
                    metadatas.append({
                        'type': 'class',
                        'name': class_name,
                        'source': 'doxygen'
                    })
                    ids.append(f"class_{class_name}_{str(uuid.uuid4())[:8]}")
                    
                    # Create documents for methods
                    for method in class_info.get('methods', []):
                        try:
                            method_name = method.get('name')
                            if not method_name:
                                self.logger.warning(f"Skipping method with no name in class {class_name}")
                                continue
                                
                            method_doc = self._create_method_document(method, class_name)
                            documents.append(method_doc)
                            metadatas.append({
                                'type': 'method',
                                'class': class_name,
                                'name': method_name,
                                'source': 'doxygen'
                            })
                            ids.append(f"method_{class_name}_{method_name}_{str(uuid.uuid4())[:8]}")
                        except Exception as e:
                            self.logger.warning(f"Error processing method in class {class_name}: {str(e)}")
                            continue
                except Exception as e:
                    self.logger.warning(f"Error processing class: {str(e)}")
                    continue
            
            # Process namespaces
            for namespace in ast_data.get('namespaces', []):
                try:
                    namespace_name = namespace.get('name')
                    if not namespace_name:
                        self.logger.warning("Skipping namespace with no name")
                        continue
                        
                    namespace_doc = self._create_namespace_document(namespace)
                    documents.append(namespace_doc)
                    metadatas.append({
                        'type': 'namespace',
                        'name': namespace_name,
                        'source': 'doxygen'
                    })
                    ids.append(f"namespace_{namespace_name}_{str(uuid.uuid4())[:8]}")
                except Exception as e:
                    self.logger.warning(f"Error processing namespace: {str(e)}")
                    continue
            
            if not documents:
                self.logger.error("No valid documents found to store in ChromaDB")
                return
                
            # Store in ChromaDB
            self.db_connector.add_documents(documents, metadatas, ids)
            self.logger.info(f"Successfully stored {len(documents)} AST documents in ChromaDB")
            
        except Exception as e:
            self.logger.error(f"Error processing AST data: {str(e)}")
            raise
            
    def _create_class_document(self, class_info: Dict) -> str:
        """Create a document string for a class"""
        doc_parts = [
            f"Class: {class_info.get('name', 'Unknown')}",
            f"Brief: {class_info.get('brief', 'No description available')}",
            f"Detailed: {class_info.get('detailed', 'No detailed description available')}",
            "\nMembers:"
        ]
        
        for member in class_info.get('members', []):
            doc_parts.append(f"- {member.get('type', 'Unknown')} {member.get('name', 'Unknown')}: {member.get('brief', 'No description')}")
            
        return "\n".join(doc_parts)
        
    def _create_method_document(self, method: Dict, class_name: str) -> str:
        """Create a document string for a method"""
        return f"""
Method: {method.get('name', 'Unknown')}
Class: {class_name}
Type: {method.get('type', 'Unknown')}
Arguments: {method.get('args', '()')}
Brief: {method.get('brief', 'No description available')}
Detailed: {method.get('detailed', 'No detailed description available')}
"""
        
    def _create_namespace_document(self, namespace: Dict) -> str:
        """Create a document string for a namespace"""
        doc_parts = [
            f"Namespace: {namespace.get('name', 'Unknown')}",
            f"Brief: {namespace.get('brief', 'No description available')}",
            f"Detailed: {namespace.get('detailed', 'No detailed description available')}",
            "\nContained Classes:"
        ]
        
        for class_info in namespace.get('classes', []):
            doc_parts.append(f"- {class_info.get('name', 'Unknown')}")
            
        doc_parts.append("\nFunctions:")
        for func in namespace.get('functions', []):
            doc_parts.append(f"- {func.get('type', 'Unknown')} {func.get('name', 'Unknown')}{func.get('args', '()')}: {func.get('brief', 'No description')}")
            
        return "\n".join(doc_parts) 