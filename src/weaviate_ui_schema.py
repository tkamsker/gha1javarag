"""
Weaviate UI Collections Schema for Iteration 14
Defines UIComponents and NavigationFlows collections with comprehensive metadata
"""

import weaviate
from typing import Dict, List, Any, Optional
import json
from dataclasses import asdict
from gwt_ui_processor import UIComponent, NavigationFlow, UIField, EventHandler, NavigationTarget
import logging

logger = logging.getLogger(__name__)

class WeaviateUISchemaManager:
    """Manages Weaviate UI collections and schema operations"""
    
    def __init__(self, client: weaviate.Client):
        self.client = client
        
    def create_ui_collections(self) -> bool:
        """Create UIComponents and NavigationFlows collections"""
        try:
            # Create UIComponents collection
            ui_components_schema = {
                "class": "UIComponents",
                "description": "GWT UI components with comprehensive metadata for modernization analysis",
                "vectorizer": "text2vec-transformers",
                "moduleConfig": {
                    "text2vec-transformers": {
                        "poolingStrategy": "masked_mean",
                        "vectorizeClassName": True
                    }
                },
                "properties": [
                    {
                        "name": "componentName",
                        "dataType": ["text"],
                        "description": "Name of the UI component",
                        "moduleConfig": {
                            "text2vec-transformers": {
                                "skip": False,
                                "vectorizePropertyName": True
                            }
                        }
                    },
                    {
                        "name": "componentType",
                        "dataType": ["text"],
                        "description": "Type of component (portlet, dialog, widget, view, panel)"
                    },
                    {
                        "name": "filePath",
                        "dataType": ["text"],
                        "description": "File system path to the component"
                    },
                    {
                        "name": "packageName",
                        "dataType": ["text"],
                        "description": "Java package name"
                    },
                    {
                        "name": "sourceCode",
                        "dataType": ["text"],
                        "description": "Complete source code of the component",
                        "moduleConfig": {
                            "text2vec-transformers": {
                                "skip": False,
                                "vectorizePropertyName": False
                            }
                        }
                    },
                    {
                        "name": "uiTemplate",
                        "dataType": ["text"],
                        "description": "UiBinder XML template if available"
                    },
                    {
                        "name": "gwtWidgets",
                        "dataType": ["text[]"],
                        "description": "List of GWT widgets used in the component"
                    },
                    {
                        "name": "businessDomains",
                        "dataType": ["text[]"],
                        "description": "Business domains the component belongs to"
                    },
                    {
                        "name": "userRoles",
                        "dataType": ["text[]"],
                        "description": "User roles that can access this component"
                    },
                    {
                        "name": "navigationTargets",
                        "dataType": ["text[]"],
                        "description": "Components this component can navigate to"
                    },
                    {
                        "name": "eventHandlers",
                        "dataType": ["text[]"],
                        "description": "Event handlers defined in the component"
                    },
                    {
                        "name": "uiFields",
                        "dataType": ["text"],
                        "description": "JSON string of UI fields metadata"
                    },
                    {
                        "name": "complexityScore",
                        "dataType": ["int"],
                        "description": "Calculated complexity score (0-100)"
                    },
                    {
                        "name": "accessibilityScore",
                        "dataType": ["int"],
                        "description": "Accessibility compliance score (0-100)"
                    },
                    {
                        "name": "modernizationPriority",
                        "dataType": ["text"],
                        "description": "Priority level for modernization (low, medium, high)"
                    },
                    {
                        "name": "migrationComplexity",
                        "dataType": ["text"],
                        "description": "Complexity of migration to modern frameworks"
                    },
                    {
                        "name": "userWorkflows",
                        "dataType": ["text[]"],
                        "description": "User workflows this component participates in"
                    },
                    {
                        "name": "performanceCharacteristics",
                        "dataType": ["text"],
                        "description": "Performance notes and characteristics"
                    },
                    {
                        "name": "responsiveCapability",
                        "dataType": ["boolean"],
                        "description": "Whether component has responsive design"
                    },
                    {
                        "name": "mobileCompatibility",
                        "dataType": ["boolean"],
                        "description": "Whether component is mobile compatible"
                    },
                    {
                        "name": "accessibilityFeatures",
                        "dataType": ["text[]"],
                        "description": "Accessibility features implemented"
                    },
                    {
                        "name": "modernizationRecommendations",
                        "dataType": ["text"],
                        "description": "Specific recommendations for modernization"
                    }
                ]
            }
            
            # Create NavigationFlows collection
            navigation_flows_schema = {
                "class": "NavigationFlows",
                "description": "User navigation patterns and workflows between UI components",
                "vectorizer": "text2vec-transformers",
                "moduleConfig": {
                    "text2vec-transformers": {
                        "poolingStrategy": "masked_mean",
                        "vectorizeClassName": True
                    }
                },
                "properties": [
                    {
                        "name": "flowName",
                        "dataType": ["text"],
                        "description": "Name of the navigation flow",
                        "moduleConfig": {
                            "text2vec-transformers": {
                                "skip": False,
                                "vectorizePropertyName": True
                            }
                        }
                    },
                    {
                        "name": "flowDescription",
                        "dataType": ["text"],
                        "description": "Detailed description of the navigation flow"
                    },
                    {
                        "name": "sourceComponent",
                        "dataType": ["text"],
                        "description": "Source component name"
                    },
                    {
                        "name": "targetComponent",
                        "dataType": ["text"],
                        "description": "Target component name"
                    },
                    {
                        "name": "transitionTrigger",
                        "dataType": ["text"],
                        "description": "What triggers this navigation"
                    },
                    {
                        "name": "userRole",
                        "dataType": ["text"],
                        "description": "User role associated with this flow"
                    },
                    {
                        "name": "businessProcess",
                        "dataType": ["text"],
                        "description": "Business process this flow supports"
                    },
                    {
                        "name": "flowComplexity",
                        "dataType": ["int"],
                        "description": "Complexity rating of the navigation flow"
                    },
                    {
                        "name": "usageFrequency",
                        "dataType": ["text"],
                        "description": "Expected usage frequency (low, medium, high)"
                    },
                    {
                        "name": "modernizationRecommendation",
                        "dataType": ["text"],
                        "description": "Recommendations for modernizing this flow"
                    },
                    {
                        "name": "userExperienceImpact",
                        "dataType": ["text"],
                        "description": "Impact on user experience"
                    },
                    {
                        "name": "mobileOptimization",
                        "dataType": ["text"],
                        "description": "Mobile optimization recommendations"
                    }
                ]
            }
            
            # Create collections
            self.client.schema.create_class(ui_components_schema)
            logger.info("Created UIComponents collection")
            
            self.client.schema.create_class(navigation_flows_schema)
            logger.info("Created NavigationFlows collection")
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating UI collections: {e}")
            return False
    
    def delete_ui_collections(self) -> bool:
        """Delete existing UI collections"""
        try:
            collections = ['UIComponents', 'NavigationFlows']
            
            for collection in collections:
                try:
                    self.client.schema.delete_class(collection)
                    logger.info(f"Deleted {collection} collection")
                except Exception as e:
                    logger.warning(f"Could not delete {collection}: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting UI collections: {e}")
            return False
    
    def store_ui_component(self, component: UIComponent) -> bool:
        """Store a UI component in Weaviate"""
        try:
            # Prepare data for Weaviate
            component_data = {
                "componentName": component.component_name,
                "componentType": component.component_type,
                "filePath": component.file_path,
                "packageName": component.package,
                "sourceCode": component.source_code,
                "uiTemplate": component.ui_template,
                "gwtWidgets": component.gwt_widgets,
                "businessDomains": component.business_domains,
                "userRoles": component.user_roles,
                "navigationTargets": [target.target_component for target in component.navigation_targets],
                "eventHandlers": [f"{handler.method}:{handler.event_type}" for handler in component.event_handlers],
                "uiFields": json.dumps([{
                    "field_name": field.field_name,
                    "widget_type": field.widget_type,
                    "annotations": field.annotations
                } for field in component.ui_fields]),
                "complexityScore": component.ui_complexity_score,
                "accessibilityScore": len(component.accessibility_features) * 20,  # Simple scoring
                "modernizationPriority": component.modernization_priority,
                "migrationComplexity": component.migration_complexity,
                "userWorkflows": self._generate_user_workflows(component),
                "performanceCharacteristics": component.performance_notes,
                "responsiveCapability": component.responsive_design,
                "mobileCompatibility": component.responsive_design,  # Assume same as responsive
                "accessibilityFeatures": component.accessibility_features,
                "modernizationRecommendations": self._generate_modernization_recommendations(component)
            }
            
            # Store in Weaviate
            self.client.data_object.create(
                data_object=component_data,
                class_name="UIComponents",
                uuid=component.component_id
            )
            
            logger.debug(f"Stored UI component: {component.component_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing UI component {component.component_name}: {e}")
            return False
    
    def store_navigation_flow(self, flow: NavigationFlow) -> bool:
        """Store a navigation flow in Weaviate"""
        try:
            flow_data = {
                "flowName": flow.flow_name,
                "flowDescription": flow.flow_description,
                "sourceComponent": flow.source_component,
                "targetComponent": flow.target_component,
                "transitionTrigger": flow.transition_trigger,
                "userRole": flow.user_role,
                "businessProcess": flow.business_process,
                "flowComplexity": flow.flow_complexity,
                "usageFrequency": flow.usage_frequency,
                "modernizationRecommendation": flow.modernization_recommendation,
                "userExperienceImpact": self._assess_ux_impact(flow),
                "mobileOptimization": self._generate_mobile_optimization_recommendations(flow)
            }
            
            self.client.data_object.create(
                data_object=flow_data,
                class_name="NavigationFlows",
                uuid=flow.flow_id
            )
            
            logger.debug(f"Stored navigation flow: {flow.flow_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing navigation flow {flow.flow_name}: {e}")
            return False
    
    def store_ui_analysis_results(self, analysis_results: Dict[str, Any]) -> Dict[str, int]:
        """Store complete UI analysis results"""
        stats = {
            'components_stored': 0,
            'flows_stored': 0,
            'errors': 0
        }
        
        # Store UI components
        for component in analysis_results['ui_components'].values():
            if self.store_ui_component(component):
                stats['components_stored'] += 1
            else:
                stats['errors'] += 1
        
        # Store navigation flows
        for flow in analysis_results['navigation_flows']:
            if self.store_navigation_flow(flow):
                stats['flows_stored'] += 1
            else:
                stats['errors'] += 1
        
        logger.info(f"UI Analysis storage complete: {stats}")
        return stats
    
    def query_ui_components(self, 
                           component_type: Optional[str] = None,
                           business_domain: Optional[str] = None,
                           modernization_priority: Optional[str] = None,
                           limit: int = 10) -> List[Dict]:
        """Query UI components with filters"""
        try:
            query = self.client.query.get("UIComponents", [
                "componentName", "componentType", "packageName", 
                "businessDomains", "modernizationPriority", "complexityScore"
            ])
            
            # Add filters
            where_filters = []
            
            if component_type:
                where_filters.append({
                    "path": ["componentType"],
                    "operator": "Equal",
                    "valueString": component_type
                })
            
            if business_domain:
                where_filters.append({
                    "path": ["businessDomains"],
                    "operator": "ContainsAny",
                    "valueStringArray": [business_domain]
                })
            
            if modernization_priority:
                where_filters.append({
                    "path": ["modernizationPriority"],
                    "operator": "Equal",
                    "valueString": modernization_priority
                })
            
            if where_filters:
                if len(where_filters) == 1:
                    query = query.where(where_filters[0])
                else:
                    query = query.where({
                        "operator": "And",
                        "operands": where_filters
                    })
            
            result = query.with_limit(limit).do()
            
            return result.get('data', {}).get('Get', {}).get('UIComponents', [])
            
        except Exception as e:
            logger.error(f"Error querying UI components: {e}")
            return []
    
    def query_navigation_flows(self, 
                              source_component: Optional[str] = None,
                              business_process: Optional[str] = None,
                              limit: int = 10) -> List[Dict]:
        """Query navigation flows with filters"""
        try:
            query = self.client.query.get("NavigationFlows", [
                "flowName", "sourceComponent", "targetComponent",
                "businessProcess", "userRole", "flowComplexity"
            ])
            
            where_filters = []
            
            if source_component:
                where_filters.append({
                    "path": ["sourceComponent"],
                    "operator": "Equal",
                    "valueString": source_component
                })
            
            if business_process:
                where_filters.append({
                    "path": ["businessProcess"],
                    "operator": "Equal",
                    "valueString": business_process
                })
            
            if where_filters:
                if len(where_filters) == 1:
                    query = query.where(where_filters[0])
                else:
                    query = query.where({
                        "operator": "And",
                        "operands": where_filters
                    })
            
            result = query.with_limit(limit).do()
            
            return result.get('data', {}).get('Get', {}).get('NavigationFlows', [])
            
        except Exception as e:
            logger.error(f"Error querying navigation flows: {e}")
            return []
    
    def get_ui_analysis_summary(self) -> Dict[str, Any]:
        """Get summary statistics of UI analysis"""
        try:
            # Get component counts by type
            components_result = self.client.query.aggregate("UIComponents").with_group_by_filter([
                "componentType"
            ]).with_fields("meta { count }").do()
            
            # Get flow counts by business process
            flows_result = self.client.query.aggregate("NavigationFlows").with_group_by_filter([
                "businessProcess"
            ]).with_fields("meta { count }").do()
            
            # Get high priority components
            high_priority = self.client.query.get("UIComponents", [
                "componentName", "modernizationPriority", "complexityScore"
            ]).where({
                "path": ["modernizationPriority"],
                "operator": "Equal",
                "valueString": "high"
            }).with_limit(20).do()
            
            summary = {
                'component_types': components_result.get('data', {}).get('Aggregate', {}),
                'business_processes': flows_result.get('data', {}).get('Aggregate', {}),
                'high_priority_components': high_priority.get('data', {}).get('Get', {}).get('UIComponents', []),
                'timestamp': json.dumps({"generated": True})  # Placeholder
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting UI analysis summary: {e}")
            return {}
    
    def _generate_user_workflows(self, component: UIComponent) -> List[str]:
        """Generate user workflows based on component characteristics"""
        workflows = []
        
        # Map business domains to workflows
        domain_workflows = {
            'customer': ['customer_registration', 'customer_management', 'customer_support'],
            'product': ['product_catalog_browsing', 'product_administration', 'service_provisioning'],
            'billing': ['invoice_generation', 'payment_processing', 'billing_administration'],
            'order': ['order_creation', 'order_management', 'order_fulfillment'],
            'support': ['ticket_creation', 'issue_resolution', 'support_administration'],
            'admin': ['system_administration', 'user_management', 'configuration']
        }
        
        for domain in component.business_domains:
            if domain in domain_workflows:
                workflows.extend(domain_workflows[domain])
        
        # Add component-type specific workflows
        if component.component_type == 'portlet':
            workflows.append('dashboard_interaction')
        elif component.component_type == 'dialog':
            workflows.append('data_entry')
        
        return list(set(workflows))
    
    def _generate_modernization_recommendations(self, component: UIComponent) -> str:
        """Generate specific modernization recommendations"""
        recommendations = []
        
        # Based on component type
        type_recommendations = {
            'portlet': 'Migrate to React/Vue card components with modern state management',
            'dialog': 'Replace with modern modal components using libraries like Material-UI Dialog',
            'view': 'Convert to modern page components with routing (React Router, Vue Router)',
            'panel': 'Replace with modern layout components (CSS Grid, Flexbox)',
            'widget': 'Migrate to reusable component library (Material-UI, Ant Design)'
        }
        
        if component.component_type in type_recommendations:
            recommendations.append(type_recommendations[component.component_type])
        
        # Based on complexity
        if component.ui_complexity_score > 70:
            recommendations.append('Consider breaking down into smaller, reusable components')
        
        # Based on accessibility
        if not component.accessibility_features:
            recommendations.append('Implement WCAG 2.1 AA accessibility standards')
        
        # Based on responsive design
        if not component.responsive_design:
            recommendations.append('Implement mobile-first responsive design patterns')
        
        return '; '.join(recommendations) if recommendations else 'Standard migration to modern framework'
    
    def _assess_ux_impact(self, flow: NavigationFlow) -> str:
        """Assess user experience impact of navigation flow"""
        if flow.flow_complexity >= 4:
            return "High - Complex navigation may confuse users"
        elif flow.flow_complexity >= 2:
            return "Medium - Moderate impact on user journey"
        else:
            return "Low - Simple navigation with minimal UX impact"
    
    def _generate_mobile_optimization_recommendations(self, flow: NavigationFlow) -> str:
        """Generate mobile optimization recommendations"""
        recommendations = []
        
        if 'dialog' in flow.source_component.lower():
            recommendations.append('Replace modal dialogs with mobile-friendly slide-up panels')
        
        if flow.flow_complexity > 3:
            recommendations.append('Simplify navigation flow for mobile users')
        
        if 'tree' in flow.source_component.lower():
            recommendations.append('Implement collapsible navigation for mobile screens')
        
        return '; '.join(recommendations) if recommendations else 'Standard mobile navigation patterns'