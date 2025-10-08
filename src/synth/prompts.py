"""
Prompt templates for PRD synthesis.
"""
from typing import List, Dict, Any

class PromptTemplates:
    """Templates for generating PRD content."""
    
    @staticmethod
    def flow_synthesis_prompt(artifacts: List[Dict[str, Any]]) -> str:
        """Generate prompt for flow synthesis."""
        context = "\n".join([artifact.get('text', '') for artifact in artifacts])
        
        return f"""You are a senior product analyst. Given these artifacts (GWT Places/Activities, UiBinder views, GWT endpoints, JS routes/XHR, JSP forms, iBATIS statements + DAO calls), produce ONE coherent user-facing flow that spans UI → API → DB.

Return JSON:
{{
 "title": "...",
 "summary": "...",
 "actors": ["Buyer","Admin"],
 "entryPoints": [{{"kind":"GWT_PLACE|JS_ROUTE|JSP","value":"orders/new"}}],
 "ui": {{"views": ["OrderView"], "fields":[{{"name":"qty","type":"number","required":true,"validation":"qty>0"}}]}},
 "api": {{"style":"RPC|RequestFactory|REST","endpoint":"/gwt.rpc|/api/orders","methods":["save(order)"], "payloadSchema":"..."}},
 "steps": ["..."], 
 "reads": ["table.column", ...], 
 "writes": ["table.column", ...],
 "navigation": {{"onSuccess":"orders/{{id}}","onError":"error dialog"}},
 "trace": {{"statements":["Order.insert"],"files":["OrderService.java:45-102","order.xml:120-164","OrderView.ui.xml:1-120","orders.js:10-84"],"routes":["orders/new","/order/create"]}}
}}

Artifacts:
<<<CONTEXT>>>
{context}
<<<CONTEXT>>>"""
    
    @staticmethod
    def requirement_synthesis_prompt(artifacts: List[Dict[str, Any]]) -> str:
        """Generate prompt for requirement synthesis."""
        context = "\n".join([artifact.get('text', '') for artifact in artifacts])
        
        return f"""You are a senior product analyst. Given these artifacts, generate functional and non-functional requirements.

Return JSON:
{{
 "functionalRequirements": [
   {{
     "id": "FR-001",
     "title": "User can create new orders",
     "description": "The system shall allow users to create new orders through the order creation form",
     "acceptanceCriteria": [
       "GIVEN a user is on the order creation page WHEN they fill out the form and click save THEN the order is created and they are redirected to the order details page",
       "GIVEN a user submits an invalid form WHEN the form is submitted THEN validation errors are displayed and the form is not submitted"
     ],
     "priority": "High",
     "trace": {{"files": ["OrderView.ui.xml", "OrderService.java"], "statements": ["Order.insert"]}}
   }}
 ],
 "nonFunctionalRequirements": [
   {{
     "id": "NFR-001",
     "title": "Response Time",
     "description": "The system shall respond to user actions within 2 seconds",
     "category": "Performance",
     "priority": "High"
   }}
 ]
}}

Artifacts:
<<<CONTEXT>>>
{context}
<<<CONTEXT>>>"""
    
    @staticmethod
    def prd_section_prompt(section: str, artifacts: List[Dict[str, Any]]) -> str:
        """Generate prompt for specific PRD sections."""
        context = "\n".join([artifact.get('text', '') for artifact in artifacts])
        
        if section == "overview":
            return f"""Generate a product overview section for a PRD based on these artifacts:

{context}

Return a markdown section with:
- Product Vision
- Key Features
- Target Users
- Success Metrics"""
        
        elif section == "features":
            return f"""Generate a features section for a PRD based on these artifacts:

{context}

Return a markdown section with:
- Feature descriptions
- User stories
- Acceptance criteria
- UI/UX considerations"""
        
        elif section == "technical":
            return f"""Generate a technical architecture section for a PRD based on these artifacts:

{context}

Return a markdown section with:
- System architecture
- Technology stack
- Integration points
- Data flow"""
        
        elif section == "frontend":
            return f"""Generate a frontend section for a PRD based on these artifacts:

{context}

Return a markdown section with:
- User interface components
- Navigation flows
- Client-side validations
- User experience patterns"""
        
        else:
            return f"""Generate content for PRD section '{section}' based on these artifacts:

{context}

Return relevant markdown content."""
    
    @staticmethod
    def traceability_prompt(artifacts: List[Dict[str, Any]]) -> str:
        """Generate prompt for traceability analysis."""
        context = "\n".join([artifact.get('text', '') for artifact in artifacts])
        
        return f"""Analyze these artifacts and create traceability mappings:

{context}

Return JSON:
{{
 "uiToApi": [
   {{"uiComponent": "OrderView.ui.xml", "apiEndpoint": "OrderService.save", "method": "POST"}}
 ],
 "apiToDb": [
   {{"apiMethod": "OrderService.save", "dbStatement": "Order.insert", "table": "orders"}}
 ],
 "uiToDb": [
   {{"uiField": "orderForm.quantity", "dbColumn": "orders.quantity", "validation": "qty > 0"}}
 ],
 "flows": [
   {{"name": "Order Creation", "components": ["OrderView", "OrderService", "orders table"], "path": "UI → API → DB"}}
 ]
}}"""
