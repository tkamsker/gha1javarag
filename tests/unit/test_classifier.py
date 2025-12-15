"""
Unit tests for file classifier.

Tests file type classification based on paths, extensions, and content.

NOTE: These tests should FAIL initially (TDD approach).
"""

import pytest
from pathlib import Path

from codeindex.services.classifier import (
    FileClassifier,
    classify_file,
    is_java_source,
    is_java_test,
    is_jsp_file,
    is_xml_config,
    is_sql_file,
    get_artifact_type,
)
from codeindex.models import ArtifactType


# Fixtures
@pytest.fixture
def classifier():
    """FileClassifier instance."""
    return FileClassifier()


@pytest.fixture
def sample_java_path():
    """Path to sample Java file."""
    return Path(__file__).parent.parent / "fixtures" / "sample_java" / "SampleClass.java"


@pytest.fixture
def sample_jsp_path():
    """Path to sample JSP file."""
    return Path(__file__).parent.parent / "fixtures" / "sample_jsp" / "SampleForm.jsp"


@pytest.fixture
def sample_xml_path():
    """Path to sample XML config file."""
    return Path(__file__).parent.parent / "fixtures" / "sample_xml" / "spring-config.xml"


@pytest.fixture
def sample_sql_path():
    """Path to sample SQL file."""
    return Path(__file__).parent.parent / "fixtures" / "sample_sql" / "schema.sql"


# Test Java source classification
class TestJavaSourceClassification:
    """Test Java source file classification."""

    def test_classify_java_source_file(self, classifier, sample_java_path):
        """Test classification of Java source file."""
        result = classifier.classify(sample_java_path)

        assert result == ArtifactType.JAVA_SOURCE

    def test_is_java_source_by_extension(self):
        """Test Java source detection by extension."""
        assert is_java_source(Path("src/main/java/com/example/Service.java"))
        assert is_java_source(Path("/path/to/MyClass.java"))

    def test_is_java_source_by_path(self):
        """Test Java source detection by path pattern."""
        assert is_java_source(Path("src/main/java/Service.java"))
        assert is_java_source(Path("project/src/main/java/util/Helper.java"))

    def test_not_java_source_test_path(self):
        """Test that test files are not classified as source."""
        assert not is_java_source(Path("src/test/java/ServiceTest.java"))
        assert not is_java_source(Path("src/test/java/TestHelper.java"))


# Test Java test classification
class TestJavaTestClassification:
    """Test Java test file classification."""

    def test_classify_test_by_path(self, classifier):
        """Test classification by test path."""
        test_path = Path("src/test/java/com/example/ServiceTest.java")
        result = classifier.classify(test_path)

        assert result == ArtifactType.JAVA_TEST

    def test_classify_test_by_name_suffix(self, classifier):
        """Test classification by Test suffix."""
        test_paths = [
            Path("src/main/java/ServiceTest.java"),
            Path("src/main/java/HelperTests.java"),
            Path("src/main/java/TestRunner.java"),
        ]

        for path in test_paths:
            result = classifier.classify(path)
            assert result == ArtifactType.JAVA_TEST

    def test_is_java_test_patterns(self):
        """Test Java test detection patterns."""
        assert is_java_test(Path("src/test/java/ServiceTest.java"))
        assert is_java_test(Path("src/test/java/TestHelper.java"))
        assert is_java_test(Path("src/main/java/FooTest.java"))
        assert is_java_test(Path("src/main/java/BarTests.java"))

    def test_not_java_test_source_file(self):
        """Test that regular source is not classified as test."""
        assert not is_java_test(Path("src/main/java/TestUtils.java"))  # Contains "Test" but not test file
        assert not is_java_test(Path("src/main/java/Service.java"))


# Test JSP classification
class TestJSPClassification:
    """Test JSP file classification."""

    def test_classify_jsp_file(self, classifier, sample_jsp_path):
        """Test classification of JSP file."""
        result = classifier.classify(sample_jsp_path)

        assert result == ArtifactType.JSP_VIEW

    def test_is_jsp_by_extension(self):
        """Test JSP detection by extension."""
        assert is_jsp_file(Path("webapp/views/index.jsp"))
        assert is_jsp_file(Path("src/main/webapp/WEB-INF/pages/form.jsp"))

    def test_jspx_files(self):
        """Test JSPX (XML JSP) file detection."""
        assert is_jsp_file(Path("webapp/views/page.jspx"))

    def test_jsp_fragment(self):
        """Test JSP fragment file detection."""
        assert is_jsp_file(Path("webapp/includes/header.jspf"))


# Test XML configuration classification
class TestXMLConfigClassification:
    """Test XML configuration file classification."""

    def test_classify_spring_config(self, classifier, sample_xml_path):
        """Test classification of Spring XML config."""
        result = classifier.classify(sample_xml_path)

        assert result == ArtifactType.XML_CONFIG

    def test_is_xml_config_by_name(self):
        """Test XML config detection by filename."""
        config_files = [
            Path("src/main/resources/applicationContext.xml"),
            Path("WEB-INF/spring-config.xml"),
            Path("META-INF/persistence.xml"),
            Path("src/main/resources/mybatis-config.xml"),
        ]

        for path in config_files:
            assert is_xml_config(path)

    def test_is_xml_config_by_location(self):
        """Test XML config detection by location."""
        assert is_xml_config(Path("src/main/resources/config.xml"))
        assert is_xml_config(Path("WEB-INF/custom.xml"))
        assert is_xml_config(Path("META-INF/services.xml"))

    def test_not_xml_config_pom(self):
        """Test that pom.xml is not classified as config."""
        assert not is_xml_config(Path("pom.xml"))
        assert not is_xml_config(Path("module/pom.xml"))


# Test SQL file classification
class TestSQLClassification:
    """Test SQL file classification."""

    def test_classify_sql_schema(self, classifier, sample_sql_path):
        """Test classification of SQL schema file."""
        result = classifier.classify(sample_sql_path)

        # Should be either SQL_SCHEMA or SQL_QUERY
        assert result in [ArtifactType.SQL_SCHEMA, ArtifactType.SQL_QUERY]

    def test_is_sql_by_extension(self):
        """Test SQL detection by extension."""
        assert is_sql_file(Path("db/schema.sql"))
        assert is_sql_file(Path("migrations/001_create_tables.sql"))

    def test_classify_schema_by_name(self, classifier):
        """Test schema classification by filename."""
        schema_files = [
            Path("db/schema.sql"),
            Path("migrations/create_tables.sql"),
            Path("db/ddl.sql"),
        ]

        for path in schema_files:
            result = classifier.classify(path)
            assert result == ArtifactType.SQL_SCHEMA

    def test_classify_query_by_name(self, classifier):
        """Test query classification by filename."""
        query_file = Path("src/main/resources/sql/queries.sql")
        result = classifier.classify(query_file)

        assert result == ArtifactType.SQL_QUERY


# Test HTML template classification
class TestHTMLTemplateClassification:
    """Test HTML template file classification."""

    def test_classify_html_template(self, classifier):
        """Test classification of HTML template."""
        html_path = Path("src/main/resources/templates/index.html")
        result = classifier.classify(html_path)

        assert result == ArtifactType.HTML_TEMPLATE

    def test_html_in_templates_dir(self, classifier):
        """Test HTML in templates directory."""
        paths = [
            Path("templates/home.html"),
            Path("src/main/resources/templates/form.html"),
            Path("webapp/templates/page.html"),
        ]

        for path in paths:
            result = classifier.classify(path)
            assert result == ArtifactType.HTML_TEMPLATE

    def test_thymeleaf_templates(self, classifier):
        """Test Thymeleaf template detection."""
        # Thymeleaf templates are typically in templates/ with .html extension
        result = classifier.classify(Path("templates/user-form.html"))
        assert result == ArtifactType.HTML_TEMPLATE


# Test properties file classification
class TestPropertiesClassification:
    """Test properties file classification."""

    def test_classify_properties_file(self, classifier):
        """Test classification of properties file."""
        props_path = Path("src/main/resources/application.properties")
        result = classifier.classify(props_path)

        assert result == ArtifactType.PROPERTIES_FILE

    def test_various_properties_files(self, classifier):
        """Test various properties file patterns."""
        props_files = [
            Path("application.properties"),
            Path("config.properties"),
            Path("messages.properties"),
            Path("database.properties"),
        ]

        for path in props_files:
            result = classifier.classify(path)
            assert result == ArtifactType.PROPERTIES_FILE


# Test JavaScript classification
class TestJavaScriptClassification:
    """Test JavaScript file classification."""

    def test_classify_javascript(self, classifier):
        """Test classification of JavaScript file."""
        js_path = Path("src/main/webapp/js/app.js")
        result = classifier.classify(js_path)

        assert result == ArtifactType.JS_SCRIPT

    def test_various_js_extensions(self, classifier):
        """Test various JS file extensions."""
        js_files = [
            Path("webapp/app.js"),
            Path("static/bundle.mjs"),
            Path("resources/script.jsx"),
        ]

        for path in js_files:
            result = classifier.classify(path)
            assert result == ArtifactType.JS_SCRIPT


# Test GWT module classification
class TestGWTModuleClassification:
    """Test GWT module file classification."""

    def test_classify_gwt_module(self, classifier):
        """Test classification of GWT module XML."""
        gwt_path = Path("src/main/java/com/example/MyApp.gwt.xml")
        result = classifier.classify(gwt_path)

        assert result == ArtifactType.GWT_MODULE

    def test_gwt_module_detection(self, classifier):
        """Test GWT module detection by naming pattern."""
        gwt_files = [
            Path("com/example/App.gwt.xml"),
            Path("src/main/java/Module.gwt.xml"),
        ]

        for path in gwt_files:
            result = classifier.classify(path)
            assert result == ArtifactType.GWT_MODULE


# Test edge cases
class TestEdgeCases:
    """Test edge cases in file classification."""

    def test_file_without_extension(self, classifier):
        """Test classification of file without extension."""
        path = Path("src/main/resources/README")
        result = classifier.classify(path)

        # Should have a fallback classification
        assert result is not None

    def test_hidden_file(self, classifier):
        """Test classification of hidden file."""
        path = Path(".gitignore")
        result = classifier.classify(path)

        assert result is not None

    def test_uppercase_extension(self, classifier):
        """Test case-insensitive extension matching."""
        path = Path("src/main/java/Service.JAVA")
        result = classifier.classify(path)

        assert result == ArtifactType.JAVA_SOURCE

    def test_multiple_dots_in_filename(self, classifier):
        """Test filename with multiple dots."""
        path = Path("application.dev.properties")
        result = classifier.classify(path)

        assert result == ArtifactType.PROPERTIES_FILE


# Test get_artifact_type helper
class TestGetArtifactType:
    """Test get_artifact_type helper function."""

    def test_get_artifact_type_java(self):
        """Test artifact type for Java file."""
        artifact_type = get_artifact_type(Path("src/main/java/Service.java"))
        assert artifact_type == ArtifactType.JAVA_SOURCE

    def test_get_artifact_type_returns_enum(self):
        """Test that function returns ArtifactType enum."""
        artifact_type = get_artifact_type(Path("test.jsp"))
        assert isinstance(artifact_type, ArtifactType)

    def test_get_artifact_type_unknown(self):
        """Test artifact type for unknown file type."""
        artifact_type = get_artifact_type(Path("random.xyz"))
        # Should return OTHER_TEXT as fallback for unknown types
        assert artifact_type == ArtifactType.OTHER_TEXT


# Test FileClassifier class methods
class TestFileClassifierMethods:
    """Test FileClassifier class methods."""

    def test_classifier_initialization(self):
        """Test FileClassifier initialization."""
        classifier = FileClassifier()
        assert classifier is not None

    def test_classify_method_exists(self, classifier):
        """Test that classify method exists."""
        assert hasattr(classifier, 'classify')
        assert callable(classifier.classify)

    def test_classify_with_string_path(self, classifier):
        """Test classify with string path (should convert to Path)."""
        result = classifier.classify("src/main/java/Service.java")
        assert result == ArtifactType.JAVA_SOURCE

    def test_classify_with_path_object(self, classifier, sample_java_path):
        """Test classify with Path object."""
        result = classifier.classify(sample_java_path)
        assert result == ArtifactType.JAVA_SOURCE

    def test_batch_classification(self, classifier):
        """Test batch classification of multiple files."""
        paths = [
            Path("src/main/java/Service.java"),
            Path("src/test/java/ServiceTest.java"),
            Path("webapp/index.jsp"),
            Path("config.properties"),
        ]

        results = [classifier.classify(path) for path in paths]

        assert len(results) == 4
        assert results[0] == ArtifactType.JAVA_SOURCE
        assert results[1] == ArtifactType.JAVA_TEST
        assert results[2] == ArtifactType.JSP_VIEW
        assert results[3] == ArtifactType.PROPERTIES_FILE


# Test classify_file standalone function
class TestClassifyFileFunction:
    """Test classify_file standalone function."""

    def test_classify_file_function_exists(self):
        """Test that classify_file function exists."""
        assert callable(classify_file)

    def test_classify_file_java(self):
        """Test classify_file with Java file."""
        result = classify_file(Path("src/main/java/App.java"))
        assert result == ArtifactType.JAVA_SOURCE

    def test_classify_file_consistent_with_classifier(self, classifier):
        """Test that standalone function matches classifier method."""
        path = Path("src/main/java/Service.java")

        func_result = classify_file(path)
        method_result = classifier.classify(path)

        assert func_result == method_result


# Test GWT Pattern Classification (T079)
class TestGwtPatternClassification:
    """Test classification of GWT-specific file patterns."""

    def test_classify_rpc_servlet(self, classifier):
        """Test classification of GWT RPC servlet."""
        path = Path("src/main/java/com/example/server/FlashInfoServletImpl.java")
        result = classifier.classify(path)

        # RPC servlets should be classified as JAVA_SOURCE
        # The GWT analyzer will handle the specific role
        assert result == ArtifactType.JAVA_SOURCE

    def test_classify_gwt_service_interface(self, classifier):
        """Test classification of GWT service interface."""
        path = Path("src/main/java/com/example/client/FlashInfoService.java")
        result = classifier.classify(path)

        assert result == ArtifactType.JAVA_SOURCE

    def test_classify_gwt_async_interface(self, classifier):
        """Test classification of GWT async service interface."""
        path = Path("src/main/java/com/example/client/FlashInfoServiceAsync.java")
        result = classifier.classify(path)

        assert result == ArtifactType.JAVA_SOURCE

    def test_classify_uibinder_xml(self, classifier):
        """Test classification of UiBinder XML template."""
        path = Path("src/main/java/com/example/client/FlashInfoEditView.ui.xml")
        result = classifier.classify(path)

        # UiBinder templates should be classified as GWT_UI_BINDER
        assert result == ArtifactType.GWT_UI_BINDER

    def test_classify_gwt_presenter(self, classifier):
        """Test classification of GWT MVP presenter."""
        path = Path("src/main/java/com/example/client/FlashAdministrationPresenter.java")
        result = classifier.classify(path)

        assert result == ArtifactType.JAVA_SOURCE

    def test_classify_gwt_view(self, classifier):
        """Test classification of GWT MVP view."""
        path = Path("src/main/java/com/example/client/FlashAdministrationView.java")
        result = classifier.classify(path)

        assert result == ArtifactType.JAVA_SOURCE

    def test_classify_shared_dto(self, classifier):
        """Test classification of shared DTO."""
        path = Path("src/main/java/com/example/shared/FlashInfoDTO.java")
        result = classifier.classify(path)

        assert result == ArtifactType.JAVA_SOURCE

    def test_classify_gwt_module_xml(self, classifier):
        """Test classification of GWT module descriptor."""
        path = Path("src/main/java/com/example/Application.gwt.xml")
        result = classifier.classify(path)

        assert result == ArtifactType.GWT_MODULE

    def test_classify_gwt_client_code(self, classifier):
        """Test classification of GWT client-side code."""
        path = Path("src/main/java/com/example/client/UserListActivity.java")
        result = classifier.classify(path)

        assert result == ArtifactType.JAVA_SOURCE

    def test_classify_gwt_place(self, classifier):
        """Test classification of GWT Place class."""
        path = Path("src/main/java/com/example/client/place/DashboardPlace.java")
        result = classifier.classify(path)

        assert result == ArtifactType.JAVA_SOURCE


class TestGwtFilePatternRecognition:
    """Test GWT-specific file pattern recognition."""

    def test_recognize_servlet_impl_pattern(self, classifier):
        """Test recognition of *ServletImpl.java pattern."""
        paths = [
            Path("src/main/java/UserServletImpl.java"),
            Path("src/main/java/FlashInfoServletImpl.java"),
            Path("src/main/java/AdminServletImpl.java"),
        ]

        for path in paths:
            result = classifier.classify(path)
            assert result == ArtifactType.JAVA_SOURCE

    def test_recognize_presenter_pattern(self, classifier):
        """Test recognition of *Presenter.java pattern."""
        paths = [
            Path("src/main/java/UserPresenter.java"),
            Path("src/main/java/DashboardPresenter.java"),
            Path("src/main/java/admin/FlashPresenter.java"),
        ]

        for path in paths:
            result = classifier.classify(path)
            assert result == ArtifactType.JAVA_SOURCE

    def test_recognize_view_pattern(self, classifier):
        """Test recognition of *View.java pattern."""
        paths = [
            Path("src/main/java/UserView.java"),
            Path("src/main/java/DashboardView.java"),
            Path("src/main/java/client/FlashView.java"),
        ]

        for path in paths:
            result = classifier.classify(path)
            assert result == ArtifactType.JAVA_SOURCE

    def test_recognize_dto_pattern(self, classifier):
        """Test recognition of *DTO.java pattern."""
        paths = [
            Path("src/main/java/shared/UserDTO.java"),
            Path("src/main/java/shared/FlashInfoDTO.java"),
            Path("src/main/java/com/example/shared/PermissionDTO.java"),
        ]

        for path in paths:
            result = classifier.classify(path)
            assert result == ArtifactType.JAVA_SOURCE

    def test_recognize_ui_xml_pattern(self, classifier):
        """Test recognition of *.ui.xml pattern."""
        paths = [
            Path("src/main/java/client/UserView.ui.xml"),
            Path("src/main/java/client/FlashEditView.ui.xml"),
            Path("src/main/java/admin/DashboardView.ui.xml"),
        ]

        for path in paths:
            result = classifier.classify(path)
            assert result == ArtifactType.GWT_UI_BINDER

    def test_recognize_gwt_xml_pattern(self, classifier):
        """Test recognition of *.gwt.xml pattern."""
        paths = [
            Path("src/main/java/Application.gwt.xml"),
            Path("src/main/java/com/example/App.gwt.xml"),
            Path("src/main/resources/Module.gwt.xml"),
        ]

        for path in paths:
            result = classifier.classify(path)
            assert result == ArtifactType.GWT_MODULE


class TestGwtPackageStructure:
    """Test classification within typical GWT package structures."""

    def test_classify_client_package_files(self, classifier):
        """Test files in typical GWT client package."""
        paths = [
            Path("src/main/java/com/example/client/UserPresenter.java"),
            Path("src/main/java/com/example/client/UserView.java"),
            Path("src/main/java/com/example/client/UserView.ui.xml"),
            Path("src/main/java/com/example/client/FlashInfoService.java"),
            Path("src/main/java/com/example/client/FlashInfoServiceAsync.java"),
        ]

        for path in paths:
            result = classifier.classify(path)
            assert result in [ArtifactType.JAVA_SOURCE, ArtifactType.GWT_UI_BINDER]

    def test_classify_server_package_files(self, classifier):
        """Test files in typical GWT server package."""
        paths = [
            Path("src/main/java/com/example/server/FlashInfoServletImpl.java"),
            Path("src/main/java/com/example/server/UserServletImpl.java"),
            Path("src/main/java/com/example/server/AdminServlet.java"),
        ]

        for path in paths:
            result = classifier.classify(path)
            assert result == ArtifactType.JAVA_SOURCE

    def test_classify_shared_package_files(self, classifier):
        """Test files in typical GWT shared package."""
        paths = [
            Path("src/main/java/com/example/shared/UserDTO.java"),
            Path("src/main/java/com/example/shared/FlashInfoDTO.java"),
            Path("src/main/java/com/example/shared/PermissionDTO.java"),
        ]

        for path in paths:
            result = classifier.classify(path)
            assert result == ArtifactType.JAVA_SOURCE
