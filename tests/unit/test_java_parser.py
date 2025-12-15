"""
Unit tests for Java source parser.

Tests parsing of Java files to extract structural information.

NOTE: These tests should FAIL initially (TDD approach).
"""

import pytest
from pathlib import Path
from typing import List, Dict

from codeindex.parsers.java_parser import (
    JavaParser,
    parse_java_file,
    extract_package,
    extract_imports,
    extract_classes,
    extract_interfaces,
    extract_methods,
    extract_annotations,
    JavaElement,
)


# Fixtures
@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory."""
    return Path(__file__).parent.parent / "fixtures" / "sample_java"


@pytest.fixture
def sample_class_path(fixtures_dir):
    """Path to SampleClass.java."""
    return fixtures_dir / "SampleClass.java"


@pytest.fixture
def sample_interface_path(fixtures_dir):
    """Path to SampleInterface.java."""
    return fixtures_dir / "SampleInterface.java"


@pytest.fixture
def annotated_class_path(fixtures_dir):
    """Path to AnnotatedClass.java."""
    return fixtures_dir / "AnnotatedClass.java"


@pytest.fixture
def abstract_class_path(fixtures_dir):
    """Path to AbstractBaseClass.java."""
    return fixtures_dir / "AbstractBaseClass.java"


@pytest.fixture
def enum_path(fixtures_dir):
    """Path to SampleEnum.java."""
    return fixtures_dir / "SampleEnum.java"


@pytest.fixture
def java_parser():
    """JavaParser instance."""
    return JavaParser()


# Test package extraction
class TestPackageExtraction:
    """Test Java package extraction."""

    def test_extract_package_from_simple_class(self, java_parser, sample_class_path):
        """Test extracting package from simple class."""
        content = sample_class_path.read_text()
        package = java_parser.extract_package(content)

        assert package == "com.example.test"

    def test_extract_package_from_interface(self, java_parser, sample_interface_path):
        """Test extracting package from interface."""
        content = sample_interface_path.read_text()
        package = java_parser.extract_package(content)

        assert package == "com.example.test.api"

    def test_extract_package_returns_none_when_missing(self, java_parser):
        """Test that missing package returns None."""
        content = "public class NoPackage { }"
        package = java_parser.extract_package(content)

        assert package is None

    def test_extract_package_handles_comments(self, java_parser):
        """Test package extraction with comments."""
        content = """
        // This is a comment
        /* Block comment */
        package com.example.commented;

        public class Test { }
        """
        package = java_parser.extract_package(content)

        assert package == "com.example.commented"


# Test import extraction
class TestImportExtraction:
    """Test Java import extraction."""

    def test_extract_imports_from_simple_class(self, java_parser, sample_class_path):
        """Test extracting imports from simple class."""
        content = sample_class_path.read_text()
        imports = java_parser.extract_imports(content)

        assert "java.util.List" in imports
        assert len(imports) >= 1

    def test_extract_imports_from_interface(self, java_parser, sample_interface_path):
        """Test extracting imports from interface."""
        content = sample_interface_path.read_text()
        imports = java_parser.extract_imports(content)

        assert "java.util.List" in imports
        assert "java.util.Optional" in imports
        assert len(imports) >= 2

    def test_extract_imports_from_annotated_class(self, java_parser, annotated_class_path):
        """Test extracting imports including annotations."""
        content = annotated_class_path.read_text()
        imports = java_parser.extract_imports(content)

        assert "org.springframework.stereotype.Service" in imports
        assert "org.springframework.beans.factory.annotation.Autowired" in imports
        assert "javax.annotation.PostConstruct" in imports

    def test_extract_imports_handles_wildcards(self, java_parser):
        """Test wildcard imports."""
        content = """
        package com.example;
        import java.util.*;
        import org.springframework.beans.*;

        public class Test { }
        """
        imports = java_parser.extract_imports(content)

        assert "java.util.*" in imports
        assert "org.springframework.beans.*" in imports

    def test_extract_imports_handles_static_imports(self, java_parser):
        """Test static imports."""
        content = """
        package com.example;
        import static java.lang.Math.PI;
        import static org.junit.Assert.*;

        public class Test { }
        """
        imports = java_parser.extract_imports(content)

        assert "java.lang.Math.PI" in imports or "java.lang.Math" in imports
        # Static imports might be extracted differently


# Test class extraction
class TestClassExtraction:
    """Test Java class extraction."""

    def test_extract_class_from_simple_file(self, java_parser, sample_class_path):
        """Test extracting class from simple file."""
        content = sample_class_path.read_text()
        classes = java_parser.extract_classes(content)

        assert len(classes) >= 1
        assert any(c['name'] == 'SampleClass' for c in classes)

    def test_extract_class_with_modifiers(self, java_parser, annotated_class_path):
        """Test extracting class with modifiers."""
        content = annotated_class_path.read_text()
        classes = java_parser.extract_classes(content)

        assert len(classes) >= 1
        class_info = next(c for c in classes if c['name'] == 'AnnotatedClass')
        assert class_info['type'] == 'class'
        assert 'public' in class_info.get('modifiers', [])

    def test_extract_abstract_class(self, java_parser, abstract_class_path):
        """Test extracting abstract class."""
        content = abstract_class_path.read_text()
        classes = java_parser.extract_classes(content)

        assert len(classes) >= 1
        class_info = next(c for c in classes if c['name'] == 'AbstractBaseClass')
        assert 'abstract' in class_info.get('modifiers', []) or class_info.get('is_abstract', False)

    def test_extract_enum(self, java_parser, enum_path):
        """Test extracting enum."""
        content = enum_path.read_text()
        classes = java_parser.extract_classes(content)

        assert len(classes) >= 1
        enum_info = next(c for c in classes if c['name'] == 'SampleEnum')
        assert enum_info['type'] == 'enum' or 'enum' in str(enum_info)


# Test interface extraction
class TestInterfaceExtraction:
    """Test Java interface extraction."""

    def test_extract_interface(self, java_parser, sample_interface_path):
        """Test extracting interface."""
        content = sample_interface_path.read_text()
        interfaces = java_parser.extract_interfaces(content)

        assert len(interfaces) >= 1
        assert any(i['name'] == 'SampleInterface' for i in interfaces)

    def test_interface_has_correct_type(self, java_parser, sample_interface_path):
        """Test that interface type is correct."""
        content = sample_interface_path.read_text()
        interfaces = java_parser.extract_interfaces(content)

        interface_info = next(i for i in interfaces if i['name'] == 'SampleInterface')
        assert interface_info['type'] == 'interface'


# Test method extraction
class TestMethodExtraction:
    """Test Java method extraction."""

    def test_extract_methods_from_class(self, java_parser, sample_class_path):
        """Test extracting methods from class."""
        content = sample_class_path.read_text()
        methods = java_parser.extract_methods(content)

        method_names = [m['name'] for m in methods]
        assert 'greet' in method_names
        assert 'increment' in method_names
        assert 'getCount' in method_names

    def test_extract_method_with_parameters(self, java_parser, sample_class_path):
        """Test extracting method parameters."""
        content = sample_class_path.read_text()
        methods = java_parser.extract_methods(content)

        greet_method = next(m for m in methods if m['name'] == 'greet')
        assert 'String' in str(greet_method.get('parameters', []))

    def test_extract_method_return_types(self, java_parser, sample_class_path):
        """Test extracting method return types."""
        content = sample_class_path.read_text()
        methods = java_parser.extract_methods(content)

        greet_method = next(m for m in methods if m['name'] == 'greet')
        assert greet_method.get('return_type') == 'String'

        increment_method = next(m for m in methods if m['name'] == 'increment')
        assert increment_method.get('return_type') == 'void'

    def test_extract_static_method(self, java_parser, abstract_class_path):
        """Test extracting static method."""
        content = abstract_class_path.read_text()
        methods = java_parser.extract_methods(content)

        static_method = next((m for m in methods if m['name'] == 'isValid'), None)
        assert static_method is not None
        assert 'static' in static_method.get('modifiers', []) or static_method.get('is_static', False)

    def test_extract_abstract_method(self, java_parser, abstract_class_path):
        """Test extracting abstract method."""
        content = abstract_class_path.read_text()
        methods = java_parser.extract_methods(content)

        abstract_method = next((m for m in methods if m['name'] == 'execute'), None)
        assert abstract_method is not None
        assert 'abstract' in abstract_method.get('modifiers', []) or abstract_method.get('is_abstract', False)


# Test annotation extraction
class TestAnnotationExtraction:
    """Test Java annotation extraction."""

    def test_extract_class_annotations(self, java_parser, annotated_class_path):
        """Test extracting class-level annotations."""
        content = annotated_class_path.read_text()
        annotations = java_parser.extract_annotations(content)

        annotation_names = [a['name'] for a in annotations]
        assert 'Service' in annotation_names or '@Service' in annotation_names
        assert 'SuppressWarnings' in annotation_names or '@SuppressWarnings' in annotation_names

    def test_extract_method_annotations(self, java_parser, annotated_class_path):
        """Test extracting method-level annotations."""
        content = annotated_class_path.read_text()
        methods = java_parser.extract_methods(content)

        # Find deprecated method
        old_method = next((m for m in methods if m['name'] == 'oldMethod'), None)
        if old_method:
            annotations = old_method.get('annotations', [])
            assert any('Deprecated' in str(a) for a in annotations)

    def test_extract_field_annotations(self, java_parser, annotated_class_path):
        """Test extracting field-level annotations."""
        content = annotated_class_path.read_text()
        annotations = java_parser.extract_annotations(content)

        # Should find @Autowired on repository field
        assert any('Autowired' in str(a) for a in annotations)


# Test full parsing
class TestFullParsing:
    """Test complete Java file parsing."""

    def test_parse_java_file_returns_dict(self, java_parser, sample_class_path):
        """Test that parse returns structured dict."""
        result = java_parser.parse_file(sample_class_path)

        assert isinstance(result, dict)
        assert 'package' in result
        assert 'imports' in result
        assert 'classes' in result or 'interfaces' in result

    def test_parse_java_file_with_path(self, java_parser, sample_class_path):
        """Test parsing from file path."""
        result = java_parser.parse_file(sample_class_path)

        assert result['package'] == 'com.example.test'
        assert len(result['imports']) >= 1
        assert len(result['classes']) >= 1

    def test_parse_java_file_with_content(self, java_parser, sample_class_path):
        """Test parsing from string content."""
        content = sample_class_path.read_text()
        result = java_parser.parse(content)

        assert result['package'] == 'com.example.test'
        assert len(result['imports']) >= 1

    def test_parse_includes_all_elements(self, java_parser, annotated_class_path):
        """Test that parsing includes all structural elements."""
        result = java_parser.parse_file(annotated_class_path)

        assert 'package' in result
        assert 'imports' in result
        assert 'classes' in result
        assert 'annotations' in result
        assert 'methods' in result or any('methods' in c for c in result['classes'])


# Test standalone functions
class TestStandaloneFunctions:
    """Test standalone parser functions."""

    def test_parse_java_file_function(self, sample_class_path):
        """Test standalone parse_java_file function."""
        result = parse_java_file(sample_class_path)

        assert isinstance(result, dict)
        assert result['package'] == 'com.example.test'

    def test_extract_package_function(self, sample_class_path):
        """Test standalone extract_package function."""
        content = sample_class_path.read_text()
        package = extract_package(content)

        assert package == 'com.example.test'

    def test_extract_imports_function(self, sample_class_path):
        """Test standalone extract_imports function."""
        content = sample_class_path.read_text()
        imports = extract_imports(content)

        assert isinstance(imports, list)
        assert 'java.util.List' in imports

    def test_extract_classes_function(self, sample_class_path):
        """Test standalone extract_classes function."""
        content = sample_class_path.read_text()
        classes = extract_classes(content)

        assert isinstance(classes, list)
        assert len(classes) >= 1


# Test error handling
class TestErrorHandling:
    """Test error handling in Java parser."""

    def test_parse_invalid_java(self, java_parser):
        """Test parsing invalid Java code."""
        invalid_content = "this is not valid Java { { {"

        # Should not crash, might return partial results
        result = java_parser.parse(invalid_content)
        assert isinstance(result, dict)

    def test_parse_empty_file(self, java_parser):
        """Test parsing empty file."""
        result = java_parser.parse("")

        assert isinstance(result, dict)
        assert result.get('package') is None or result.get('package') == ''

    def test_parse_nonexistent_file(self, java_parser):
        """Test parsing non-existent file."""
        with pytest.raises(FileNotFoundError):
            java_parser.parse_file(Path("/nonexistent/file.java"))

    def test_parse_handles_unicode(self, java_parser):
        """Test parsing file with unicode characters."""
        content = """
        package com.example.unicode;

        public class UnicodeTest {
            // Comment with unicode: 你好
            private String greeting = "Привет";
        }
        """
        result = java_parser.parse(content)

        assert result['package'] == 'com.example.unicode'


# Test edge cases
class TestEdgeCases:
    """Test edge cases in Java parsing."""

    def test_parse_nested_classes(self, java_parser):
        """Test parsing nested classes."""
        content = """
        package com.example;

        public class Outer {
            public class Inner {
                public void innerMethod() {}
            }

            public static class StaticNested {
                public void nestedMethod() {}
            }
        }
        """
        result = java_parser.parse(content)

        classes = result.get('classes', [])
        # Should find at least the outer class
        assert len(classes) >= 1

    def test_parse_multiple_classes_in_file(self, java_parser):
        """Test parsing multiple classes in one file."""
        content = """
        package com.example;

        class FirstClass {
            public void method1() {}
        }

        class SecondClass {
            public void method2() {}
        }
        """
        result = java_parser.parse(content)

        classes = result.get('classes', [])
        assert len(classes) >= 2

    def test_parse_generic_types(self, java_parser):
        """Test parsing generic types."""
        content = """
        package com.example;

        import java.util.List;
        import java.util.Map;

        public class GenericClass<T> {
            private List<String> items;
            private Map<String, T> mapping;

            public T getValue(String key) {
                return mapping.get(key);
            }
        }
        """
        result = java_parser.parse(content)

        assert result['package'] == 'com.example'
        # Generics should be handled gracefully


# Integration-like tests
class TestIntegration:
    """Test integration of parser components."""

    def test_full_workflow_simple_class(self, java_parser, sample_class_path):
        """Test complete parsing workflow."""
        result = java_parser.parse_file(sample_class_path)

        # Verify package
        assert result['package'] == 'com.example.test'

        # Verify imports
        assert 'java.util.List' in result['imports']

        # Verify class
        classes = result.get('classes', [])
        assert len(classes) >= 1
        sample_class = next(c for c in classes if c['name'] == 'SampleClass')

        # Verify methods
        methods = result.get('methods', []) or sample_class.get('methods', [])
        method_names = [m['name'] for m in methods]
        assert 'greet' in method_names
        assert 'getCount' in method_names

    def test_full_workflow_interface(self, java_parser, sample_interface_path):
        """Test parsing interface file."""
        result = java_parser.parse_file(sample_interface_path)

        assert result['package'] == 'com.example.test.api'
        assert len(result['imports']) >= 2

        interfaces = result.get('interfaces', [])
        assert len(interfaces) >= 1

    def test_full_workflow_annotated_class(self, java_parser, annotated_class_path):
        """Test parsing annotated class."""
        result = java_parser.parse_file(annotated_class_path)

        # Verify annotations
        annotations = result.get('annotations', [])
        assert len(annotations) >= 2

        # Verify imports include annotation packages
        imports = result.get('imports', [])
        assert any('springframework' in imp for imp in imports)


# ===================================================================
# Tests for Validation Annotation Extraction (T043)
# ===================================================================

class TestValidationAnnotationExtraction:
    """Test validation annotation extraction for DTOs (T043)."""

    def test_extract_validation_annotations_not_null(self):
        """Test extraction of @NotNull annotation."""
        from src.codeindex.parsers.java_parser import extract_validation_annotations

        fixture_path = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        annotations = extract_validation_annotations(fixture_path)

        # Should find @NotNull annotations
        not_null_annotations = [a for a in annotations if a['type'] == 'NotNull']
        assert len(not_null_annotations) > 0

        # Each annotation should have field name
        for ann in not_null_annotations:
            assert 'field_name' in ann
            assert 'type' in ann

    def test_extract_validation_annotations_size(self):
        """Test extraction of @Size annotation with parameters."""
        from src.codeindex.parsers.java_parser import extract_validation_annotations

        fixture_path = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        annotations = extract_validation_annotations(fixture_path)

        # Should find @Size annotations
        size_annotations = [a for a in annotations if a['type'] == 'Size']
        assert len(size_annotations) > 0

        # @Size should have min/max parameters
        for ann in size_annotations:
            assert 'field_name' in ann
            # Should have at least one of min or max
            assert 'parameters' in ann
            params = ann['parameters']
            assert 'min' in params or 'max' in params

    def test_extract_validation_annotations_pattern(self):
        """Test extraction of @Pattern annotation with regexp."""
        from src.codeindex.parsers.java_parser import extract_validation_annotations

        fixture_path = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        annotations = extract_validation_annotations(fixture_path)

        # Should find @Pattern annotations
        pattern_annotations = [a for a in annotations if a['type'] == 'Pattern']
        assert len(pattern_annotations) > 0

        # @Pattern should have regexp parameter
        for ann in pattern_annotations:
            assert 'parameters' in ann
            assert 'regexp' in ann['parameters']

    def test_extract_validation_annotations_email(self):
        """Test extraction of @Email annotation."""
        from src.codeindex.parsers.java_parser import extract_validation_annotations

        fixture_path = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        annotations = extract_validation_annotations(fixture_path)

        # Should find @Email annotations
        email_annotations = [a for a in annotations if a['type'] == 'Email']
        assert len(email_annotations) > 0

    def test_extract_validation_annotations_valid(self):
        """Test extraction of @Valid annotation for nested DTOs."""
        from src.codeindex.parsers.java_parser import extract_validation_annotations

        fixture_path = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/nested-dto.java")

        annotations = extract_validation_annotations(fixture_path)

        # Should find @Valid annotations on nested DTO fields
        valid_annotations = [a for a in annotations if a['type'] == 'Valid']
        assert len(valid_annotations) > 0

    def test_extract_validation_annotations_min_max(self):
        """Test extraction of @Min and @Max annotations."""
        from src.codeindex.parsers.java_parser import extract_validation_annotations

        fixture_path = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        annotations = extract_validation_annotations(fixture_path)

        # Should find @Min or @Max annotations if present
        min_max_annotations = [a for a in annotations if a['type'] in ['Min', 'Max']]

        # Each should have value parameter
        for ann in min_max_annotations:
            assert 'parameters' in ann
            assert 'value' in ann['parameters']

    def test_extract_validation_annotations_not_empty(self):
        """Test extraction of @NotEmpty annotation."""
        from src.codeindex.parsers.java_parser import extract_validation_annotations

        fixture_path = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        annotations = extract_validation_annotations(fixture_path)

        # All annotations should be in list format
        assert isinstance(annotations, list)

        # Each annotation should have required fields
        for ann in annotations:
            assert 'type' in ann
            assert 'field_name' in ann

    def test_extract_validation_annotations_empty_file(self):
        """Test that empty or non-existent files return empty list."""
        from src.codeindex.parsers.java_parser import extract_validation_annotations

        # Non-existent file
        non_existent = Path("tests/fixtures/dto-classes/nonexistent.java")

        annotations = extract_validation_annotations(non_existent)

        # Should return empty list, not raise error
        assert isinstance(annotations, list)
        assert len(annotations) == 0

    def test_annotation_parameter_parsing(self):
        """Test that annotation parameters are correctly parsed."""
        from src.codeindex.parsers.java_parser import extract_validation_annotations

        fixture_path = Path("tests/fixtures/dto-classes/src/main/java/com/example/dto/standard-dto.java")

        annotations = extract_validation_annotations(fixture_path)

        # Find an annotation with parameters
        size_annotations = [a for a in annotations if a['type'] == 'Size']

        if size_annotations:
            ann = size_annotations[0]
            params = ann['parameters']

            # Parameters should be dict
            assert isinstance(params, dict)

            # Values should be properly typed (int, string, etc.)
            for key, value in params.items():
                assert isinstance(key, str)
                # Value can be int, str, bool, etc.
                assert value is not None
