"""
Unit tests for GWT Model Analyzer.

Tests:
- T065: DTO field extraction
- T066: Validation rule extraction (@NotNull, @Size, @Email, @Pattern)
- T067: GWT serialization check
- T068: Nested DTO detection
"""

import pytest
from pathlib import Path

# These imports will fail initially until GwtModelAnalyzer is implemented
try:
    from codeindex.services.gwt_model_analyzer import GwtModelAnalyzer
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False


@pytest.fixture
def gwt_fixtures_dir():
    """Get path to GWT test fixtures."""
    return Path(__file__).parent.parent / "fixtures" / "gwt"


@pytest.fixture
def flash_info_dto_content(gwt_fixtures_dir):
    """Load FlashInfoDTO.java content."""
    file_path = gwt_fixtures_dir / "FlashInfoDTO.java"
    return file_path.read_text(encoding='utf-8')


@pytest.fixture
def user_dto_content(gwt_fixtures_dir):
    """Load UserDTO.java content."""
    file_path = gwt_fixtures_dir / "UserDTO.java"
    return file_path.read_text(encoding='utf-8')


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtModelAnalyzer not yet implemented")
class TestDtoFieldExtraction:
    """T065: Test DTO field extraction."""

    def test_extract_all_fields(self, gwt_fixtures_dir, flash_info_dto_content):
        """Test extraction of all DTO fields."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        result = analyzer.analyze(file_path, flash_info_dto_content)

        assert 'fields' in result
        fields = result['fields']

        # FlashInfoDTO has 11 fields
        assert len(fields) >= 10

        # Check field names
        field_names = [f['name'] for f in fields]
        assert 'id' in field_names
        assert 'title' in field_names
        assert 'description' in field_names
        assert 'category' in field_names
        assert 'active' in field_names

    def test_extract_field_types(self, gwt_fixtures_dir, flash_info_dto_content):
        """Test that field types are correctly extracted."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        result = analyzer.analyze(file_path, flash_info_dto_content)
        fields = result['fields']

        # Find specific fields and check types
        id_field = next(f for f in fields if f['name'] == 'id')
        assert id_field['type'] == 'Long'

        title_field = next(f for f in fields if f['name'] == 'title')
        assert title_field['type'] == 'String'

        active_field = next(f for f in fields if f['name'] == 'active')
        assert active_field['type'] == 'Boolean'

    def test_extract_field_with_javadoc(self, gwt_fixtures_dir, flash_info_dto_content):
        """Test extraction of field Javadoc comments."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        result = analyzer.analyze(file_path, flash_info_dto_content)
        fields = result['fields']

        # Find field with Javadoc
        title_field = next(f for f in fields if f['name'] == 'title')
        assert 'description' in title_field
        # Should contain some of the Javadoc text
        assert title_field['description'] is not None


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtModelAnalyzer not yet implemented")
class TestValidationRuleExtraction:
    """T066: Test validation rule extraction."""

    def test_extract_not_null_constraint(self, gwt_fixtures_dir, flash_info_dto_content):
        """Test extraction of @NotNull validation."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        result = analyzer.analyze(file_path, flash_info_dto_content)
        fields = result['fields']

        # Find field with @NotNull
        title_field = next(f for f in fields if f['name'] == 'title')
        assert 'validation_rules' in title_field
        rules = title_field['validation_rules']

        # Should have @NotNull rule
        not_null_rule = next((r for r in rules if r['type'] == 'NotNull'), None)
        assert not_null_rule is not None
        assert 'message' in not_null_rule
        assert 'required' in not_null_rule['message'].lower()

    def test_extract_size_constraint(self, gwt_fixtures_dir, flash_info_dto_content):
        """Test extraction of @Size validation."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        result = analyzer.analyze(file_path, flash_info_dto_content)
        fields = result['fields']

        # Find field with @Size
        title_field = next(f for f in fields if f['name'] == 'title')
        rules = title_field['validation_rules']

        # Should have @Size rule with min/max
        size_rule = next((r for r in rules if r['type'] == 'Size'), None)
        assert size_rule is not None
        assert 'min' in size_rule
        assert 'max' in size_rule
        assert size_rule['min'] == 3
        assert size_rule['max'] == 100

    def test_extract_email_constraint(self, gwt_fixtures_dir, user_dto_content):
        """Test extraction of @Email validation."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "UserDTO.java"

        result = analyzer.analyze(file_path, user_dto_content)
        fields = result['fields']

        # Find email field
        email_field = next(f for f in fields if f['name'] == 'email')
        rules = email_field['validation_rules']

        # Should have @Email rule
        email_rule = next((r for r in rules if r['type'] == 'Email'), None)
        assert email_rule is not None

    def test_extract_pattern_constraint(self, gwt_fixtures_dir, user_dto_content):
        """Test extraction of @Pattern validation."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "UserDTO.java"

        result = analyzer.analyze(file_path, user_dto_content)
        fields = result['fields']

        # Find username field with @Pattern
        username_field = next(f for f in fields if f['name'] == 'username')
        rules = username_field['validation_rules']

        # Should have @Pattern rule with regexp
        pattern_rule = next((r for r in rules if r['type'] == 'Pattern'), None)
        assert pattern_rule is not None
        assert 'regexp' in pattern_rule
        assert 'alphanumeric' in pattern_rule.get('message', '').lower()

    def test_multiple_validation_rules(self, gwt_fixtures_dir, user_dto_content):
        """Test field with multiple validation rules."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "UserDTO.java"

        result = analyzer.analyze(file_path, user_dto_content)
        fields = result['fields']

        # Username has @NotNull, @Size, and @Pattern
        username_field = next(f for f in fields if f['name'] == 'username')
        rules = username_field['validation_rules']

        assert len(rules) >= 3
        rule_types = [r['type'] for r in rules]
        assert 'NotNull' in rule_types
        assert 'Size' in rule_types
        assert 'Pattern' in rule_types


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtModelAnalyzer not yet implemented")
class TestGwtSerializationCheck:
    """T067: Test GWT serialization check."""

    def test_detect_is_serializable(self, gwt_fixtures_dir, flash_info_dto_content):
        """Test detection of IsSerializable interface."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        result = analyzer.analyze(file_path, flash_info_dto_content)

        assert 'gwt_serializable' in result
        assert result['gwt_serializable'] is True

    def test_detect_java_serializable(self, gwt_fixtures_dir, flash_info_dto_content):
        """Test detection of Serializable interface."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        result = analyzer.analyze(file_path, flash_info_dto_content)

        assert 'java_serializable' in result
        assert result['java_serializable'] is True

    def test_detect_serial_version_uid(self, gwt_fixtures_dir, flash_info_dto_content):
        """Test detection of serialVersionUID field."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        result = analyzer.analyze(file_path, flash_info_dto_content)

        assert 'has_serial_version_uid' in result
        assert result['has_serial_version_uid'] is True

    def test_detect_default_constructor(self, gwt_fixtures_dir, flash_info_dto_content):
        """Test detection of default constructor."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        result = analyzer.analyze(file_path, flash_info_dto_content)

        assert 'has_default_constructor' in result
        assert result['has_default_constructor'] is True

    def test_warn_missing_default_constructor(self, tmp_path):
        """Test warning for missing default constructor."""
        analyzer = GwtModelAnalyzer()

        # DTO without default constructor
        content = """
        package com.example;
        import com.google.gwt.user.client.rpc.IsSerializable;

        public class BadDTO implements IsSerializable {
            private String name;

            // No default constructor!
            public BadDTO(String name) {
                this.name = name;
            }
        }
        """

        file_path = tmp_path / "BadDTO.java"
        file_path.write_text(content)

        result = analyzer.analyze(file_path, content)

        assert result['has_default_constructor'] is False
        assert 'warnings' in result
        assert any('default constructor' in w.lower() for w in result['warnings'])


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtModelAnalyzer not yet implemented")
class TestNestedDtoDetection:
    """T068: Test nested DTO detection."""

    def test_detect_nested_dto_fields(self, gwt_fixtures_dir, user_dto_content):
        """Test detection of nested DTO references."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "UserDTO.java"

        result = analyzer.analyze(file_path, user_dto_content)

        assert 'nested_dtos' in result
        nested = result['nested_dtos']

        # UserDTO references several nested DTOs
        assert len(nested) >= 4

        nested_names = [n['name'] for n in nested]
        assert 'UserProfileDTO' in nested_names
        assert 'AddressDTO' in nested_names
        assert 'PermissionDTO' in nested_names
        assert 'ProjectDTO' in nested_names

    def test_detect_list_of_dtos(self, gwt_fixtures_dir, user_dto_content):
        """Test detection of List<DTO> fields."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "UserDTO.java"

        result = analyzer.analyze(file_path, user_dto_content)
        fields = result['fields']

        # Find permissions field (List<PermissionDTO>)
        permissions_field = next((f for f in fields if f['name'] == 'permissions'), None)
        assert permissions_field is not None
        assert 'List' in permissions_field['type']
        assert 'PermissionDTO' in permissions_field['type']

    def test_detect_set_of_dtos(self, gwt_fixtures_dir, user_dto_content):
        """Test detection of Set<DTO> fields."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "UserDTO.java"

        result = analyzer.analyze(file_path, user_dto_content)
        fields = result['fields']

        # Find projects field (Set<ProjectDTO>)
        projects_field = next((f for f in fields if f['name'] == 'projects'), None)
        assert projects_field is not None
        assert 'Set' in projects_field['type']
        assert 'ProjectDTO' in projects_field['type']

    def test_detect_inner_class_dtos(self, gwt_fixtures_dir, user_dto_content):
        """Test detection of inner class DTOs."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "UserDTO.java"

        result = analyzer.analyze(file_path, user_dto_content)

        # UserDTO has inner classes: UserProfileDTO, AddressDTO, etc.
        assert 'inner_classes' in result
        inner_classes = result['inner_classes']

        assert len(inner_classes) >= 4

        inner_names = [ic['name'] for ic in inner_classes]
        assert 'UserProfileDTO' in inner_names
        assert 'AddressDTO' in inner_names


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtModelAnalyzer not yet implemented")
class TestGwtModelAnalyzerIntegration:
    """Integration tests for complete DTO analysis."""

    def test_analyze_complete_dto(self, gwt_fixtures_dir, flash_info_dto_content):
        """Test complete analysis of DTO."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        result = analyzer.analyze(file_path, flash_info_dto_content)

        # Check structure
        assert result['gwt_role'] == 'shared_dto'
        assert 'dto_name' in result
        assert result['dto_name'] == 'FlashInfoDTO'
        assert 'package' in result
        assert 'fields' in result
        assert 'gwt_serializable' in result
        assert 'java_serializable' in result
        assert 'has_default_constructor' in result

    def test_can_analyze_dto_files(self, gwt_fixtures_dir):
        """Test that analyzer can identify DTO files."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        assert analyzer.can_analyze(file_path) is True

    def test_cannot_analyze_non_dto_files(self, gwt_fixtures_dir):
        """Test that analyzer rejects non-DTO files."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"

        assert analyzer.can_analyze(file_path) is False

    def test_complex_dto_with_nested_references(self, gwt_fixtures_dir, user_dto_content):
        """Test analysis of complex DTO with nested references."""
        analyzer = GwtModelAnalyzer()
        file_path = gwt_fixtures_dir / "UserDTO.java"

        result = analyzer.analyze(file_path, user_dto_content)

        # Should have fields, nested DTOs, and inner classes
        assert len(result['fields']) >= 10
        assert len(result['nested_dtos']) >= 4
        assert len(result['inner_classes']) >= 4

        # Should detect multiple validation rules
        total_rules = sum(len(f['validation_rules']) for f in result['fields'])
        assert total_rules >= 5  # Multiple fields have validation
