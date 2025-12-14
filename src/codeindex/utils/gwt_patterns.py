"""
GWT Pattern Matching Utilities

Provides utilities for detecting GWT patterns in Java codebases, including:
- GWT application detection
- File naming pattern matching
- RPC servlet identification
- MVP component classification

This module implements the GwtPatternDetector interface from the contracts.
"""

import logging
import re
from pathlib import Path
from typing import Optional, List, Tuple
from enum import Enum


logger = logging.getLogger(__name__)


class GwtRole(str, Enum):
    """GWT-specific artifact roles."""
    RPC_SERVLET = "rpc_servlet"
    PRESENTER = "presenter"
    VIEW = "view"
    UI_BINDER = "ui_binder"
    SHARED_DTO = "shared_dto"
    GWT_MODULE = "gwt_module"


class MvpBindingType(str, Enum):
    """MVP presenter-view binding detection strategy."""
    DISPLAY_INTERFACE = "display_interface"      # 90% confidence
    SEPARATE_INTERFACE = "separate_interface"    # 85% confidence
    NAMING_CONVENTION = "naming_convention"      # 70% confidence


# ============================================================================
# File Pattern Detection
# ============================================================================

def is_gwt_rpc_servlet(file_path: Path) -> Tuple[bool, float]:
    """
    Check if file matches GWT RPC servlet patterns.

    Args:
        file_path: Path to Java file

    Returns:
        Tuple of (is_servlet, confidence_score)

    Confidence scoring:
    - 0.95: *ServletImpl.java (standard GWT naming)
    - 0.85: *Servlet.java (alternative naming)
    - 0.80: *Service.java in *.server.* package
    - 0.00: No match
    """
    filename = file_path.name

    if filename.endswith("ServletImpl.java"):
        return (True, 0.95)
    elif filename.endswith("Servlet.java") and not filename.startswith("Remote"):
        return (True, 0.85)
    elif filename.endswith("Service.java") and ".server." in str(file_path):
        return (True, 0.80)

    return (False, 0.0)


def is_gwt_presenter(file_path: Path) -> bool:
    """
    Check if file matches GWT presenter pattern.

    Args:
        file_path: Path to Java file

    Returns:
        True if file is a GWT presenter
    """
    return file_path.name.endswith("Presenter.java")


def is_gwt_view(file_path: Path) -> bool:
    """
    Check if file matches GWT view pattern.

    Args:
        file_path: Path to Java file

    Returns:
        True if file is a GWT view
    """
    return file_path.name.endswith("View.java")


def is_uibinder_template(file_path: Path) -> bool:
    """
    Check if file is a UiBinder XML template.

    Args:
        file_path: Path to XML file

    Returns:
        True if file is a UiBinder template
    """
    return file_path.suffix == ".xml" and file_path.stem.endswith(".ui")


def is_gwt_module_descriptor(file_path: Path) -> bool:
    """
    Check if file is a GWT module descriptor.

    Args:
        file_path: Path to XML file

    Returns:
        True if file is a GWT module descriptor
    """
    return file_path.name.endswith(".gwt.xml")


def is_shared_dto(file_path: Path) -> bool:
    """
    Check if file is a shared DTO.

    Args:
        file_path: Path to Java file

    Returns:
        True if file is in shared package and ends with DTO.java,
        or if it ends with DTO.java and contains GWT serialization markers
    """
    # Standard check: DTO file in shared package
    if file_path.name.endswith("DTO.java") and ".shared." in str(file_path):
        return True

    # Fallback: Check content for GWT serialization patterns
    if file_path.name.endswith("DTO.java"):
        try:
            content = file_path.read_text(encoding='utf-8')
            return any([
                'IsSerializable' in content,
                'implements Serializable' in content,
                'serialVersionUID' in content
            ])
        except Exception:
            pass

    return False


def classify_gwt_file(file_path: Path) -> Optional[GwtRole]:
    """
    Classify a file as a specific GWT role.

    Args:
        file_path: Path to file

    Returns:
        GwtRole if file matches a GWT pattern, None otherwise
    """
    if is_gwt_module_descriptor(file_path):
        return GwtRole.GWT_MODULE
    elif is_uibinder_template(file_path):
        return GwtRole.UI_BINDER
    elif is_gwt_rpc_servlet(file_path)[0]:
        return GwtRole.RPC_SERVLET
    elif is_gwt_presenter(file_path):
        return GwtRole.PRESENTER
    elif is_gwt_view(file_path):
        return GwtRole.VIEW
    elif is_shared_dto(file_path):
        return GwtRole.SHARED_DTO

    return None


# ============================================================================
# Application Detection
# ============================================================================

def is_gwt_application(source_dir: Path) -> bool:
    """
    Detect if codebase is a GWT application.

    Indicators (FR-001):
    - Presence of *.gwt.xml module descriptors
    - GWT imports in Java files
    - client/server/shared directory structure

    Args:
        source_dir: Root of source directory

    Returns:
        True if GWT application detected
    """
    # Check for GWT module descriptors
    gwt_modules = list(source_dir.rglob("*.gwt.xml"))
    if gwt_modules:
        logger.debug(f"Found {len(gwt_modules)} GWT module descriptors")
        return True

    # Check for characteristic directory structure
    has_client = any(source_dir.rglob("client"))
    has_server = any(source_dir.rglob("server"))
    has_shared = any(source_dir.rglob("shared"))

    if has_client and has_server and has_shared:
        logger.debug("Found client/server/shared directory structure")
        return True

    # Check for GWT imports in Java files (sample first 10 files)
    java_files = list(source_dir.rglob("*.java"))[:10]
    gwt_import_pattern = re.compile(r'import\s+com\.google\.gwt\.')

    for java_file in java_files:
        try:
            content = java_file.read_text(encoding='utf-8')
            if gwt_import_pattern.search(content):
                logger.debug(f"Found GWT imports in {java_file}")
                return True
        except Exception:
            continue

    return False


def get_gwt_version(source_dir: Path) -> Optional[str]:
    """
    Detect GWT version from module descriptor or POM.

    Args:
        source_dir: Root of source directory

    Returns:
        GWT version string or None
    """
    # Check pom.xml for GWT dependency version
    pom_files = list(source_dir.rglob("pom.xml"))
    gwt_version_pattern = re.compile(r'<gwt\.version>([^<]+)</gwt\.version>')
    gwt_dependency_pattern = re.compile(
        r'<groupId>com\.google\.gwt</groupId>\s*<artifactId>[^<]+</artifactId>\s*<version>([^<]+)</version>',
        re.DOTALL
    )

    for pom_file in pom_files:
        try:
            content = pom_file.read_text(encoding='utf-8')

            # Try property first
            match = gwt_version_pattern.search(content)
            if match:
                version = match.group(1)
                logger.debug(f"Found GWT version {version} in {pom_file}")
                return version

            # Try dependency version
            match = gwt_dependency_pattern.search(content)
            if match:
                version = match.group(1)
                logger.debug(f"Found GWT version {version} in {pom_file}")
                return version
        except Exception:
            continue

    return None


# ============================================================================
# Content Pattern Detection
# ============================================================================

def contains_remote_service_servlet(content: str) -> bool:
    """
    Check if Java content extends RemoteServiceServlet.

    Args:
        content: Java source code

    Returns:
        True if content extends RemoteServiceServlet
    """
    return re.search(r'extends\s+RemoteServiceServlet', content) is not None


def contains_remote_service_interface(content: str) -> bool:
    """
    Check if Java content extends RemoteService.

    Args:
        content: Java source code

    Returns:
        True if content extends RemoteService
    """
    return re.search(r'extends\s+RemoteService', content) is not None


def contains_display_interface(content: str) -> bool:
    """
    Check if Java content has inner Display interface (MVP pattern).

    Args:
        content: Java source code

    Returns:
        True if content has Display interface
    """
    return re.search(r'interface\s+Display', content) is not None


def extract_presenter_name_from_view(view_name: str) -> str:
    """
    Extract presenter name from view name using naming convention.

    Args:
        view_name: View class name (e.g., "UserListView")

    Returns:
        Presenter class name (e.g., "UserListPresenter")
    """
    if view_name.endswith("View"):
        return view_name[:-4] + "Presenter"
    return view_name + "Presenter"


def extract_view_name_from_presenter(presenter_name: str) -> str:
    """
    Extract view name from presenter name using naming convention.

    Args:
        presenter_name: Presenter class name (e.g., "UserListPresenter")

    Returns:
        View class name (e.g., "UserListView")
    """
    if presenter_name.endswith("Presenter"):
        return presenter_name[:-9] + "View"
    return presenter_name + "View"


# ============================================================================
# Namespace URIs
# ============================================================================

UIBINDER_NAMESPACE = "urn:ui:com.google.gwt.uibinder"
GWT_WIDGETS_NAMESPACE = "urn:import:com.google.gwt.user.client.ui"


def get_gwt_namespaces() -> List[str]:
    """
    Get list of GWT XML namespace URIs.

    Returns:
        List of namespace URIs
    """
    return [UIBINDER_NAMESPACE, GWT_WIDGETS_NAMESPACE]
