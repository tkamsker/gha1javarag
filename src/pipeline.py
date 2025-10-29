"""Main pipeline orchestrator for requirements extraction"""
import json
from pathlib import Path
from typing import Dict, List
from crewai import Crew, Process

from src.config import Config
from src.utils.logger import setup_logger
from src.utils.ollama_client import OllamaClient
from src.utils.weaviate_client import WeaviateClient
from src.agents.step1_agents import create_step1_agents
from src.agents.step2_agents import create_step2_agents
from src.agents.step3_agents import create_step3_agents

logger = setup_logger("pipeline")


class RequirementsExtractionPipeline:
    """Main pipeline for requirements extraction"""
    
    def __init__(self):
        Config.ensure_output_dirs()
        self.ollama = OllamaClient()
        self.weaviate = WeaviateClient()
        self.step1_agents = create_step1_agents(self.ollama, self.weaviate)
        self.step2_agents = create_step2_agents(self.weaviate, self.ollama)
        self.step3_agents = create_step3_agents(self.ollama)
    
    def run_step1(self) -> Dict:
        """Run Step 1: Source Discovery & AI Extraction"""
        logger.info("=" * 80)
        logger.info("STEP 1: Source Discovery & AI Extraction")
        logger.info("=" * 80)
        
        # Get source files
        source_reader_tool = self.step1_agents["tools"]["source_reader"]
        discovery_result = source_reader_tool._run(str(Config.JAVA_SOURCE_DIR))
        
        projects = discovery_result.get("projects", {})
        total_files = discovery_result.get("total_files", 0)
        
        logger.info(f"Discovered {total_files} files across {len(projects)} projects")
        
        # Process each file
        file_extractor_tool = self.step1_agents["tools"]["file_extractor"]
        data_store_tool = self.step1_agents["tools"]["data_store"]
        
        processed_files = {}
        extracted_data = {}  # Store extracted info as fallback
        for project_name, files in projects.items():
            logger.info(f"\nProcessing project: {project_name} ({len(files)} files)")
            processed_files[project_name] = []
            extracted_data[project_name] = []
            
            for file_info in files:
                file_path = file_info["path"]
                file_type = file_info["type"]
                
                try:
                    # Extract information
                    extracted_info = file_extractor_tool._run(file_path, project_name)
                    
                    # Store extracted data for Step 2 fallback
                    extracted_data[project_name].append({
                        "filePath": file_path,
                        "fileType": file_type,
                        "project": project_name,
                        "extractedInfo": extracted_info
                    })
                    
                    # Store in Weaviate (may fail, but we have fallback)
                    uuid = data_store_tool._run(
                        file_path=file_path,
                        project=project_name,
                        file_type=file_type,
                        extracted_info=extracted_info
                    )
                    
                    processed_files[project_name].append({
                        "path": file_path,
                        "uuid": uuid,
                        "status": "processed"
                    })
                    
                    logger.debug(f"Processed: {file_path}")
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
                    processed_files[project_name].append({
                        "path": file_path,
                        "status": "failed",
                        "error": str(e)
                    })
        
        # Save processing log and extracted data (fallback for Step 2)
        Config.BUILD_DIR.mkdir(parents=True, exist_ok=True)
        log_file = Config.BUILD_DIR / "step1_processed.json"
        log_file.write_text(json.dumps(processed_files, indent=2), encoding='utf-8')
        
        extracted_file = Config.BUILD_DIR / "step1_extracted_data.json"
        extracted_file.write_text(json.dumps(extracted_data, indent=2), encoding='utf-8')
        logger.debug(f"Saved extracted data to {extracted_file} (Step 2 fallback)")
        
        logger.info(f"\nStep 1 complete. Processed {total_files} files.")
        return {
            "projects": list(projects.keys()),
            "processed_files": processed_files
        }
    
    def run_step2(self, step1_result: Dict) -> Dict:
        """Run Step 2: Project Structuring & Deep Analysis"""
        logger.info("=" * 80)
        logger.info("STEP 2: Project Structuring & Deep Analysis")
        logger.info("=" * 80)
        
        projects = step1_result.get("projects", [])
        structured_projects = {}
        
        project_structurer_tool = self.step2_agents["tools"]["project_structurer"]
        dao_dto_analyzer_tool = self.step2_agents["tools"]["dao_dto_analyzer"]
        service_linker_tool = self.step2_agents["tools"]["service_linker"]
        frontend_analyzer_tool = self.step2_agents["tools"]["frontend_analyzer"]
        linkage_tool = self.step2_agents["tools"]["linkage"]
        
        for project in projects:
            logger.info(f"\nStructuring project: {project}")
            
            # Structure project - try Weaviate first, fallback to local file
            project_structure = project_structurer_tool._run(project)
            
            # Fallback: if Weaviate returned no files, use local extracted data
            if not project_structure.get("files"):
                logger.warning(f"No files found in Weaviate for {project}, using fallback extracted data")
                extracted_file = Config.BUILD_DIR / "step1_extracted_data.json"
                if extracted_file.exists():
                    try:
                        fallback_data = json.loads(extracted_file.read_text(encoding='utf-8'))
                        project_files = fallback_data.get(project, [])
                        logger.info(f"Loaded {len(project_files)} files from fallback data")
                        
                        # Rebuild structure with fallback data
                        project_structure["files"] = project_files
                        
                        # Re-categorize files with fallback data
                        for file_info in project_files:
                            file_type = file_info.get("fileType", "")
                            extracted = file_info.get("extractedInfo", {})
                            
                            if file_type == "java":
                                classes = extracted.get("classes", [])
                                if not classes:
                                    logger.debug(f"No classes extracted from {file_info.get('filePath')}")
                                
                                for cls in classes:
                                    class_name = cls.get("name", "").lower()
                                    purpose = str(cls.get("purpose", "")).upper()
                                    
                                    entity_data = {
                                        "className": cls.get("name", ""),
                                        "purpose": cls.get("purpose", ""),
                                        "filePath": file_info.get("filePath", ""),
                                        "methods": cls.get("methods", []),
                                        "fields": cls.get("fields", []),
                                        "annotations": cls.get("annotations", [])
                                    }
                                    
                                    if purpose == "DAO" or "dao" in class_name or class_name.endswith("dao"):
                                        project_structure["entities"]["daos"].append(entity_data)
                                    elif purpose == "DTO" or "dto" in class_name or class_name.endswith("dto"):
                                        project_structure["entities"]["dtos"].append(entity_data)
                                    elif purpose == "SERVICE" or "service" in class_name:
                                        project_structure["entities"]["services"].append(entity_data)
                                    elif purpose == "CONTROLLER" or "controller" in class_name:
                                        project_structure["entities"]["controllers"].append(entity_data)
                                    elif purpose == "ENTITY" or "@Entity" in str(cls.get("annotations", [])):
                                        project_structure["entities"]["entities"].append(entity_data)
                                    else:
                                        project_structure["entities"]["entities"].append(entity_data)
                            elif file_type in ["jsp", "html"]:
                                project_structure["entities"]["ui_files"].append(extracted)
                            elif file_type == "sql":
                                project_structure["entities"]["sql_files"].append(extracted)
                    except Exception as e:
                        logger.error(f"Error loading fallback data: {e}")
            
            # Analyze DAOs/DTOs
            dao_dto_analysis = dao_dto_analyzer_tool._run(project_structure)
            
            # Link services
            service_api = service_linker_tool._run(project_structure, dao_dto_analysis)
            
            # Analyze frontend
            frontend_analysis = frontend_analyzer_tool._run(project_structure, service_api)
            
            # Resolve linkages
            linkage_result = linkage_tool._run(project_structure, frontend_analysis, service_api)
            
            structured_projects[project] = {
                "structure": project_structure,
                "dao_dto_analysis": dao_dto_analysis,
                "service_api": service_api,
                "frontend_analysis": frontend_analysis,
                "linkage": linkage_result
            }
            
            # Save structured JSON
            output_dir = Config.OUTPUT_DIR / project
            output_dir.mkdir(parents=True, exist_ok=True)
            json_file = output_dir / "requirements_json.json"
            json_file.write_text(json.dumps(structured_projects[project], indent=2, default=str), encoding='utf-8')
            
            logger.info(f"Structured data saved to {json_file}")
        
        logger.info(f"\nStep 2 complete. Structured {len(projects)} projects.")
        return structured_projects
    
    def run_step3(self, step2_result: Dict) -> Dict:
        """Run Step 3: Requirements Synthesis & Target Solution Mapping"""
        logger.info("=" * 80)
        logger.info("STEP 3: Requirements Synthesis & Target Solution Mapping")
        logger.info("=" * 80)
        
        requirements_writer_tool = self.step3_agents["tools"]["requirements_writer"]
        solution_mapper_tool = self.step3_agents["tools"]["solution_mapper"]
        review_tool = self.step3_agents["tools"]["reviewer"]
        
        results = {}
        
        for project, structured_data in step2_result.items():
            logger.info(f"\nGenerating requirements for: {project}")
            
            # Write requirements
            requirements_file = requirements_writer_tool._run(project, structured_data)
            
            # Create mapping
            mapping_file = solution_mapper_tool._run(project, requirements_file)
            
            # Review
            review_result = review_tool._run(requirements_file, mapping_file)
            
            results[project] = {
                "requirements_file": requirements_file,
                "mapping_file": mapping_file,
                "review": review_result
            }
            
            logger.info(f"Requirements generated for {project}")
        
        logger.info(f"\nStep 3 complete. Generated requirements for {len(results)} projects.")
        return results
    
    def run(self) -> Dict:
        """Run the complete pipeline"""
        logger.info("Starting Requirements Extraction Pipeline")
        logger.info(f"Source synchronization: {Config.JAVA_SOURCE_DIR}")
        logger.info(f"Output directory: {Config.OUTPUT_DIR}")
        
        try:
            # Step 1
            step1_result = self.run_step1()
            
            # Step 2
            step2_result = self.run_step2(step1_result)
            
            # Step 3
            step3_result = self.run_step3(step2_result)
            
            # Final summary
            summary = {
                "step1": step1_result,
                "step2": step2_result,
                "step3": step3_result,
                "projects": list(step1_result.get("projects", []))
            }
            
            summary_file = Config.OUTPUT_DIR / "pipeline_summary.json"
            summary_file.write_text(json.dumps(summary, indent=2, default=str), encoding='utf-8')
            
            logger.info("\n" + "=" * 80)
            logger.info("PIPELINE COMPLETE")
            logger.info("=" * 80)
            logger.info(f"Summary saved to: {summary_file}")
            
            return summary
        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
            raise
        finally:
            self.weaviate.close()
    
    def close(self):
        """Close connections"""
        self.weaviate.close()

