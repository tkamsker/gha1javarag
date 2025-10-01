"""
Heuristic-based metadata classification to enrich files for requirements generation.
Implements a lightweight approximation of iteration11.md classification without LLM calls.
"""

from typing import Dict, List


def classify_file(path: str, language: str, content: str) -> Dict[str, object]:
    """Return enhanced classification metadata for a file.

    Fields roughly aligned with iteration11.md EnhancedFileClassification subset.
    """
    path_lower = path.lower()
    content_lower = (content or "").lower()

    architectural_layer = _guess_layer(path_lower, language, content_lower)
    component_type = _guess_component(path_lower, language, content_lower)
    technology_stack = _detect_tech(content_lower, path_lower)

    exposes_api = any(k in content_lower for k in ["@restcontroller", "@controller", "@path(", "@getmapping", "@postmapping"]) or \
        ("/api/" in path_lower)
    consumes_api = any(k in content_lower for k in ["resttemplate", "webclient", "httpclient", "$.ajax", "fetch("])
    database_interactions = any(k in content_lower for k in ["@entity", "entitymanager", "sessionfactory", "mybatis", "ibatis", "jdbc", "sqlsession"]) or \
        (language in ["sql", "xml"] and ("select" in content_lower or "insert" in content_lower or "update" in content_lower))

    confidence = 0.6
    if component_type != "unknown" or architectural_layer != "unknown":
        confidence = 0.8

    return {
        "architectural_layer": architectural_layer,
        "component_type": component_type,
        "confidence_score": confidence,
        "technology_stack": technology_stack,
        "design_patterns": _detect_patterns(content_lower),
        "primary_purpose": _primary_purpose_hint(path_lower, language),
        "secondary_purposes": [],
        "business_domain": _guess_domain(path_lower),
        "dependencies": [],
        "exposes_api": exposes_api,
        "consumes_api": consumes_api,
        "database_interactions": database_interactions,
        "complexity_indicators": _complexity_hints(content_lower),
        "potential_issues": [],
        "refactoring_suggestions": [],
    }


def _guess_layer(path_lower: str, language: str, content_lower: str) -> str:
    if any(x in path_lower for x in ["/test/", "\\test\\", "tests", "_test."]):
        return "test"
    if language in ["jsp", "html", "javascript", "css"]:
        return "frontend"
    if any(x in path_lower for x in ["controller", "rest", "servlet", "/api/"]):
        return "backend_service"
    if any(x in path_lower for x in ["/dao/", "/repository/"]):
        return "data_access"
    if any(x in path_lower for x in ["/entity/", "/model/", "/domain/"]):
        return "persistence"
    if any(x in path_lower for x in ["/batch/", "scheduler", "job"]):
        return "batch_process"
    if language in ["xml", "properties"] or any(x in path_lower for x in ["config", "applicationcontext", ".gwt.xml"]):
        return "configuration"
    if any(x in path_lower for x in ["/security/", "security"]) or "springsecurity" in content_lower:
        return "security"
    if any(x in content_lower for x in ["@client", "kafka", "jms", "rabbitmq"]) or any(x in path_lower for x in ["/client/", "/integration/"]):
        return "integration"
    return "backend_service" if language == "java" else "unknown"


def _guess_component(path_lower: str, language: str, content_lower: str) -> str:
    if language == "jsp":
        return "jsp_page"
    if language == "javascript":
        return "javascript"
    if language == "css":
        return "css_stylesheet"
    if language == "html":
        return "html_template"
    if language == "sql":
        return "database_script"
    if "controller" in path_lower or "@controller" in content_lower or "@restcontroller" in content_lower:
        return "rest_controller"
    if "service" in path_lower or "@service" in content_lower:
        return "service_layer"
    if "repository" in path_lower or "@repository" in content_lower:
        return "repository"
    if "/dao/" in path_lower or "dao" in path_lower:
        return "dao"
    if "@entity" in content_lower or "/entity/" in path_lower:
        return "entity"
    if "dto" in path_lower:
        return "dto"
    if "servlet" in path_lower or "extends httpservlet" in content_lower:
        return "servlet"
    return "unknown"


def _detect_tech(content_lower: str, path_lower: str) -> List[str]:
    tech = []
    if any(k in content_lower for k in ["@controller", "@service", "@repository", "applicationcontext"]):
        tech.append("spring_framework")
    if "@entity" in content_lower or "javax.persistence" in content_lower or ".jpa" in content_lower:
        tech.append("jpa")
    if "hibernate" in content_lower:
        tech.append("hibernate")
    if "mybatis" in content_lower or "ibatis" in content_lower:
        tech.append("mybatis")
    if path_lower.endswith(".jsp") or "<%" in content_lower:
        tech.append("jsp")
    if "jstl" in content_lower:
        tech.append("jstl")
    if "jquery" in content_lower:
        tech.append("jquery")
    if "@springbootapplication" in content_lower:
        tech.append("spring_boot")
    return tech


def _detect_patterns(content_lower: str) -> List[str]:
    patterns = []
    if "@repository" in content_lower:
        patterns.append("repository")
    if "@service" in content_lower:
        patterns.append("service_layer")
    if "model" in content_lower and "view" in content_lower and "controller" in content_lower:
        patterns.append("mvc")
    return patterns


def _primary_purpose_hint(path_lower: str, language: str) -> str:
    if language == "jsp":
        return "Presentation template"
    if "controller" in path_lower:
        return "Handle HTTP requests"
    if "service" in path_lower:
        return "Business logic"
    if "repository" in path_lower or "dao" in path_lower:
        return "Data access"
    if language == "sql":
        return "Database DDL/DML"
    return "Source file"


def _guess_domain(path_lower: str) -> str:
    # crude domain hints from folder names
    for token in ["product", "quote", "customer", "opportunity", "sales", "billing"]:
        if token in path_lower:
            return token
    return None


def _complexity_hints(content_lower: str) -> List[str]:
    hints = []
    if content_lower.count(" if ") + content_lower.count(" for ") + content_lower.count(" while ") > 50:
        hints.append("many_control_structures")
    if len(content_lower) > 200_000:
        hints.append("very_large_file")
    return hints


