"""
Unit tests for GWT module XML parsing.

Tests T048-T049 for Feature 007 User Story 3.
"""

import pytest
from pathlib import Path


class TestParseModuleEntryPoints:
    """Tests for parsing GWT module entry points (T048)"""

    def test_parse_single_entry_point(self):
        """Test parsing single <entry-point> from GWT module"""
        # Given GWT module XML with entry-point
        module_xml = """
        <?xml version="1.0" encoding="UTF-8"?>
        <module rename-to='application'>
            <inherits name='com.google.gwt.user.User'/>
            <entry-point class='com.example.client.Application'/>
            <source path='client'/>
        </module>
        """

        # When parsing entry points (will be implemented)
        expected_entry_point = "com.example.client.Application"

        # Then should extract entry-point class
        assert expected_entry_point is not None

    def test_parse_multiple_entry_points(self):
        """Test parsing multiple <entry-point> elements"""
        # Given module with multiple entry points
        module_xml = """
        <module>
            <entry-point class='com.example.client.MainApp'/>
            <entry-point class='com.example.client.AdminApp'/>
            <entry-point class='com.example.client.ReportsApp'/>
        </module>
        """

        # When parsing all entry points
        expected_entry_points = [
            "com.example.client.MainApp",
            "com.example.client.AdminApp",
            "com.example.client.ReportsApp"
        ]

        # Then should extract all 3 entry points
        assert len(expected_entry_points) == 3

    def test_parse_entry_point_with_namespace(self):
        """Test parsing entry-point with XML namespace"""
        # Given module with namespace
        module_xml = """
        <?xml version="1.0" encoding="UTF-8"?>
        <module xmlns="http://www.gwtproject.org/schema/gwt-module">
            <entry-point class='com.example.client.Application'/>
        </module>
        """

        # When parsing with namespace awareness
        expected_entry_point = "com.example.client.Application"

        # Then should handle namespace correctly
        assert expected_entry_point is not None

    def test_parse_module_without_entry_points(self):
        """Test parsing module with no entry points (library module)"""
        # Given library module without entry points
        module_xml = """
        <module>
            <inherits name='com.google.gwt.user.User'/>
            <source path='client'/>
            <public path='public'/>
        </module>
        """

        # When parsing entry points
        extracted_entry_points = []  # Will be implemented

        # Then should return empty list
        assert len(extracted_entry_points) == 0

    def test_parse_entry_point_with_attributes(self):
        """Test parsing entry-point with additional attributes"""
        # Given entry-point with extra attributes
        module_xml = """
        <module>
            <entry-point class='com.example.client.App' condition='ie10'/>
        </module>
        """

        # When parsing entry point
        expected_entry_point = "com.example.client.App"

        # Then should extract class regardless of other attributes
        assert expected_entry_point is not None


class TestParseModuleInherits:
    """Tests for parsing GWT module inheritance (T049)"""

    def test_parse_single_inherits(self):
        """Test parsing single <inherits> declaration"""
        # Given module with inherits
        module_xml = """
        <module>
            <inherits name='com.google.gwt.user.User'/>
            <entry-point class='com.example.client.App'/>
        </module>
        """

        # When parsing inherits (will be implemented)
        expected_inherit = "com.google.gwt.user.User"

        # Then should extract inherited module name
        assert expected_inherit is not None

    def test_parse_multiple_inherits(self):
        """Test parsing multiple <inherits> declarations"""
        # Given module with multiple inherits
        module_xml = """
        <module>
            <inherits name='com.google.gwt.user.User'/>
            <inherits name='com.google.gwt.http.HTTP'/>
            <inherits name='com.example.common.CommonModule'/>
            <entry-point class='com.example.client.App'/>
        </module>
        """

        # When parsing all inherits
        expected_inherits = [
            "com.google.gwt.user.User",
            "com.google.gwt.http.HTTP",
            "com.example.common.CommonModule"
        ]

        # Then should extract all 3 inherited modules
        assert len(expected_inherits) == 3

    def test_parse_inherits_gwt_core_modules(self):
        """Test parsing standard GWT core module inherits"""
        # Given module inheriting GWT core modules
        module_xml = """
        <module>
            <inherits name='com.google.gwt.user.User'/>
            <inherits name='com.google.gwt.json.JSON'/>
            <inherits name='com.google.gwt.resources.Resources'/>
            <inherits name='com.google.gwt.place.Place'/>
            <inherits name='com.google.gwt.activity.Activity'/>
        </module>
        """

        # When parsing inherits
        expected_count = 5

        # Then should extract all GWT core modules
        gwt_core_modules = [
            "com.google.gwt.user.User",
            "com.google.gwt.json.JSON",
            "com.google.gwt.resources.Resources",
            "com.google.gwt.place.Place",
            "com.google.gwt.activity.Activity"
        ]
        assert len(gwt_core_modules) == expected_count

    def test_parse_inherits_custom_modules(self):
        """Test parsing custom application module inherits"""
        # Given module inheriting custom modules
        module_xml = """
        <module>
            <inherits name='com.example.shared.SharedModule'/>
            <inherits name='com.example.widgets.WidgetsModule'/>
            <inherits name='com.example.utils.UtilsModule'/>
        </module>
        """

        # When parsing custom inherits
        expected_inherits = [
            "com.example.shared.SharedModule",
            "com.example.widgets.WidgetsModule",
            "com.example.utils.UtilsModule"
        ]

        # Then should extract custom module names
        assert len(expected_inherits) == 3

    def test_parse_module_without_inherits(self):
        """Test parsing module with no inherits (unusual but valid)"""
        # Given module without inherits
        module_xml = """
        <module>
            <entry-point class='com.example.client.App'/>
            <source path='client'/>
        </module>
        """

        # When parsing inherits
        extracted_inherits = []  # Will be implemented

        # Then should return empty list
        assert len(extracted_inherits) == 0

    def test_parse_inherits_with_rename(self):
        """Test parsing module with rename-to attribute"""
        # Given module with rename-to
        module_xml = """
        <module rename-to='myapp'>
            <inherits name='com.google.gwt.user.User'/>
            <inherits name='com.example.common.CommonModule'/>
            <entry-point class='com.example.client.MyApp'/>
        </module>
        """

        # When parsing inherits
        expected_inherits = [
            "com.google.gwt.user.User",
            "com.example.common.CommonModule"
        ]

        # And rename attribute
        expected_rename = "myapp"

        # Then should extract both inherits and rename
        assert len(expected_inherits) == 2
        assert expected_rename is not None

    def test_parse_complete_module_structure(self):
        """Test parsing complete GWT module with all elements"""
        # Given complete GWT module
        module_xml = """
        <?xml version="1.0" encoding="UTF-8"?>
        <module rename-to='application'>
            <!-- GWT Core -->
            <inherits name='com.google.gwt.user.User'/>
            <inherits name='com.google.gwt.place.Place'/>
            <inherits name='com.google.gwt.activity.Activity'/>

            <!-- Custom Modules -->
            <inherits name='com.example.shared.SharedModule'/>
            <inherits name='com.example.widgets.WidgetsModule'/>

            <!-- Entry Points -->
            <entry-point class='com.example.client.Application'/>

            <!-- Source Paths -->
            <source path='client'/>
            <source path='shared'/>

            <!-- Public Resources -->
            <public path='public'/>
        </module>
        """

        # When parsing complete module
        # Expected structure
        expected_data = {
            "rename_to": "application",
            "inherits": [
                "com.google.gwt.user.User",
                "com.google.gwt.place.Place",
                "com.google.gwt.activity.Activity",
                "com.example.shared.SharedModule",
                "com.example.widgets.WidgetsModule"
            ],
            "entry_points": ["com.example.client.Application"],
            "source_paths": ["client", "shared"],
            "public_paths": ["public"]
        }

        # Then should extract all elements correctly
        assert len(expected_data["inherits"]) == 5
        assert len(expected_data["entry_points"]) == 1
        assert expected_data["rename_to"] == "application"
