"""
Unit tests for GWT RPC Analyzer.

Tests:
- T014: GWT RPC pattern detection
- T015: RPC method extraction (javalang path)
- T016: RPC method extraction (regex fallback)
- T017: DTO reference extraction
"""

import pytest
from pathlib import Path

# These imports will fail initially until GwtRpcAnalyzer is implemented
try:
    from codeindex.services.gwt_rpc_analyzer import GwtRpcAnalyzer
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False


@pytest.fixture
def gwt_fixtures_dir():
    """Get path to GWT test fixtures."""
    return Path(__file__).parent.parent / "fixtures" / "gwt"


@pytest.fixture
def servlet_impl_content(gwt_fixtures_dir):
    """Load FlashInfoServletImpl.java content."""
    file_path = gwt_fixtures_dir / "FlashInfoServletImpl.java"
    return file_path.read_text(encoding='utf-8')


@pytest.fixture
def service_interface_content(gwt_fixtures_dir):
    """Load FlashInfoService.java content."""
    file_path = gwt_fixtures_dir / "FlashInfoService.java"
    return file_path.read_text(encoding='utf-8')


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtRpcAnalyzer not yet implemented")
class TestGwtRpcPatternDetection:
    """T014: Test GWT RPC pattern detection."""

    def test_can_analyze_servlet_impl(self, gwt_fixtures_dir):
        """Test that analyzer recognizes *ServletImpl.java files."""
        analyzer = GwtRpcAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoServletImpl.java"

        assert analyzer.can_analyze(file_path) is True

    def test_can_analyze_servlet(self, gwt_fixtures_dir, tmp_path):
        """Test that analyzer recognizes *Servlet.java files."""
        analyzer = GwtRpcAnalyzer()

        # Create a temporary servlet file
        servlet_file = tmp_path / "UserServlet.java"
        servlet_file.write_text("public class UserServlet extends RemoteServiceServlet {}")

        assert analyzer.can_analyze(servlet_file) is True

    def test_cannot_analyze_non_servlet(self, gwt_fixtures_dir, tmp_path):
        """Test that analyzer rejects non-servlet files."""
        analyzer = GwtRpcAnalyzer()

        # Create a non-servlet file
        regular_file = tmp_path / "UserDTO.java"
        regular_file.write_text("public class UserDTO {}")

        assert analyzer.can_analyze(regular_file) is False

    def test_get_gwt_role(self):
        """Test that analyzer returns correct GWT role."""
        from codeindex.utils.gwt_patterns import GwtRole

        analyzer = GwtRpcAnalyzer()
        assert analyzer.get_gwt_role() == GwtRole.RPC_SERVLET


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtRpcAnalyzer not yet implemented")
class TestRpcMethodExtractionJavalang:
    """T015: Test RPC method extraction using javalang."""

    def test_extract_public_methods(self, gwt_fixtures_dir, servlet_impl_content):
        """Test extraction of all public RPC methods."""
        analyzer = GwtRpcAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoServletImpl.java"

        methods = analyzer.extract_rpc_methods(file_path, servlet_impl_content)

        # Should extract 6 public methods (not private helpers)
        assert len(methods) >= 5  # At minimum, the main RPC methods
        method_names = [m['name'] for m in methods]
        assert 'createFlashInfo' in method_names
        assert 'updateFlashInfo' in method_names
        assert 'deleteFlashInfo' in method_names
        assert 'getAllFlashInfo' in method_names
        assert 'getFlashInfoById' in method_names

        # Private methods should not be included
        assert 'generateId' not in method_names
        assert 'validateDTO' not in method_names

    def test_extract_method_signatures(self, gwt_fixtures_dir, servlet_impl_content):
        """Test that method signatures include return types and parameters."""
        analyzer = GwtRpcAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoServletImpl.java"

        methods = analyzer.extract_rpc_methods(file_path, servlet_impl_content)

        # Find createFlashInfo method
        create_method = next(m for m in methods if m['name'] == 'createFlashInfo')

        assert create_method['return_type'] == 'FlashInfoDTO'
        assert len(create_method['parameters']) == 1
        assert create_method['parameters'][0]['name'] == 'dto'
        assert create_method['parameters'][0]['type'] == 'FlashInfoDTO'
        assert 'RemoteException' in create_method['exceptions']

    def test_extract_method_with_multiple_parameters(self, tmp_path):
        """Test extraction of methods with multiple parameters."""
        analyzer = GwtRpcAnalyzer()

        # Create a servlet with multi-param method
        content = """
        public class TestServlet extends RemoteServiceServlet {
            public String searchFlashInfo(String query, int page, int size) {
                return null;
            }
        }
        """

        file_path = tmp_path / "TestServlet.java"
        file_path.write_text(content)

        methods = analyzer.extract_rpc_methods(file_path, content)

        assert len(methods) == 1
        method = methods[0]
        assert method['name'] == 'searchFlashInfo'
        assert len(method['parameters']) == 3
        assert method['parameters'][0]['type'] in ['String', 'java.lang.String']
        assert method['parameters'][1]['type'] == 'int'
        assert method['parameters'][2]['type'] == 'int'


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtRpcAnalyzer not yet implemented")
class TestRpcMethodExtractionRegexFallback:
    """T016: Test RPC method extraction using regex fallback."""

    def test_regex_fallback_on_malformed_java(self, tmp_path):
        """Test that regex fallback works when javalang fails."""
        analyzer = GwtRpcAnalyzer()

        # Create malformed Java (missing closing brace)
        content = """
        public class BrokenServlet extends RemoteServiceServlet {
            public String testMethod(String param) {
                return "test";
            // Missing closing brace
        """

        file_path = tmp_path / "BrokenServlet.java"
        file_path.write_text(content)

        # Should not raise exception, should use regex fallback
        methods = analyzer.extract_rpc_methods(file_path, content)

        # Regex should still extract the method
        assert len(methods) >= 1
        if methods:
            assert methods[0]['name'] == 'testMethod'

    def test_regex_extracts_basic_signatures(self, tmp_path):
        """Test that regex fallback extracts basic method signatures."""
        analyzer = GwtRpcAnalyzer()

        content = """
        public class SimpleServlet extends RemoteServiceServlet {
            public UserDTO getUser(Long id) throws RemoteException {
                return null;
            }

            public boolean deleteUser(Long id) {
                return true;
            }
        }
        """

        file_path = tmp_path / "SimpleServlet.java"
        file_path.write_text(content)

        # Force regex path by passing malformed content
        methods = analyzer._parse_with_regex(content)

        assert len(methods) >= 2
        method_names = [m['name'] for m in methods]
        assert 'getUser' in method_names
        assert 'deleteUser' in method_names


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtRpcAnalyzer not yet implemented")
class TestDtoReferenceExtraction:
    """T017: Test DTO reference extraction."""

    def test_extract_referenced_dtos(self, gwt_fixtures_dir, servlet_impl_content):
        """Test extraction of all DTO class names used in RPC methods."""
        analyzer = GwtRpcAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoServletImpl.java"

        methods = analyzer.extract_rpc_methods(file_path, servlet_impl_content)
        dtos = analyzer.extract_referenced_dtos(methods)

        # FlashInfoDTO should be referenced multiple times
        assert 'FlashInfoDTO' in dtos
        # Each DTO should appear only once (unique)
        assert len(dtos) == len(set(dtos))

    def test_identify_dto_from_parameters(self):
        """Test that DTOs are identified from method parameters."""
        analyzer = GwtRpcAnalyzer()

        methods = [
            {
                'name': 'createUser',
                'return_type': 'UserDTO',
                'parameters': [
                    {'name': 'user', 'type': 'UserDTO', 'is_dto': True}
                ],
                'exceptions': []
            }
        ]

        dtos = analyzer.extract_referenced_dtos(methods)

        assert 'UserDTO' in dtos

    def test_identify_dto_from_return_types(self):
        """Test that DTOs are identified from return types."""
        analyzer = GwtRpcAnalyzer()

        methods = [
            {
                'name': 'getUsers',
                'return_type': 'List<UserDTO>',
                'parameters': [],
                'exceptions': []
            }
        ]

        dtos = analyzer.extract_referenced_dtos(methods)

        assert 'UserDTO' in dtos

    def test_identify_service_interface(self, gwt_fixtures_dir, servlet_impl_content):
        """Test identification of service interface."""
        analyzer = GwtRpcAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoServletImpl.java"

        interface_name = analyzer.identify_service_interface(file_path, servlet_impl_content)

        assert interface_name == 'FlashInfoService'


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtRpcAnalyzer not yet implemented")
class TestGwtRpcAnalyzerIntegration:
    """Integration tests for complete analyzer workflow."""

    def test_analyze_complete_servlet(self, gwt_fixtures_dir, servlet_impl_content):
        """Test complete analysis of servlet file."""
        analyzer = GwtRpcAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoServletImpl.java"

        result = analyzer.analyze(file_path, servlet_impl_content, semantic_data=None)

        # Check structure
        assert result['gwt_role'] == 'rpc_servlet'
        assert 'servlet_name' in result
        assert result['servlet_name'] == 'FlashInfoServletImpl'
        assert 'service_interface' in result
        assert result['service_interface'] == 'FlashInfoService'
        assert 'rpc_methods' in result
        assert len(result['rpc_methods']) >= 5
        assert 'referenced_dtos' in result
        assert 'FlashInfoDTO' in result['referenced_dtos']

    def test_analyze_returns_valid_metadata(self, gwt_fixtures_dir, servlet_impl_content):
        """Test that analyze returns metadata matching data model schema."""
        analyzer = GwtRpcAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoServletImpl.java"

        result = analyzer.analyze(file_path, servlet_impl_content)

        # Validate against data model schema
        assert isinstance(result['rpc_methods'], list)
        for method in result['rpc_methods']:
            assert 'name' in method
            assert 'return_type' in method
            assert 'parameters' in method
            assert 'exceptions' in method
            assert 'visibility' in method
            assert method['visibility'] == 'public'
