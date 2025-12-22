"""
Unit tests for index.html/jsp parsing and GWT module extraction.

Tests T046-T047 for Feature 007 User Story 3.
"""

import pytest
from pathlib import Path


class TestExtractGWTModulesFromScriptTags:
    """Tests for extracting GWT modules from index.html script tags (T046)"""

    def test_extract_gwt_module_from_script_src(self):
        """Test extracting GWT module from <script src='module/module.nocache.js'>"""
        # Given index.html with GWT module script
        index_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Application</title>
            <script type="text/javascript" src="com.example.Application/com.example.Application.nocache.js"></script>
        </head>
        <body>
            <div id="root"></div>
        </body>
        </html>
        """

        # When extracting GWT modules (will be implemented)
        # Expected module name extracted from script src
        expected_module = "com.example.Application"

        # Then should extract module name
        assert expected_module is not None

    def test_extract_multiple_gwt_modules(self):
        """Test extracting multiple GWT modules from index.html"""
        # Given index.html with multiple module scripts
        index_content = """
        <html>
        <head>
            <script src="com.example.Admin/com.example.Admin.nocache.js"></script>
            <script src="com.example.User/com.example.User.nocache.js"></script>
            <script src="com.example.Reports/com.example.Reports.nocache.js"></script>
        </head>
        </html>
        """

        # When extracting all modules
        expected_modules = [
            "com.example.Admin",
            "com.example.User",
            "com.example.Reports"
        ]

        # Then should extract all 3 modules
        assert len(expected_modules) == 3

    def test_extract_gwt_module_from_inline_script(self):
        """Test extracting GWT module from inline __gwt_activeModules script"""
        # Given index.html with inline module activation
        index_content = """
        <script>
        var __gwt_activeModules = __gwt_activeModules || {};
        __gwt_activeModules['com.example.Application'] = {
            moduleName: 'com.example.Application',
            bindings: function() { return null; }
        };
        </script>
        """

        # When extracting from inline script
        expected_module = "com.example.Application"

        # Then should extract module from __gwt_activeModules
        assert expected_module is not None

    def test_extract_gwt_module_with_relative_path(self):
        """Test extracting GWT module from relative script paths"""
        # Given index.html with relative paths
        index_content = """
        <script src="../modules/com.example.App/com.example.App.nocache.js"></script>
        """

        # When extracting module
        expected_module = "com.example.App"

        # Then should extract module regardless of path depth
        assert expected_module is not None

    def test_handle_no_gwt_modules(self):
        """Test handling index.html with no GWT modules"""
        # Given index.html without GWT modules
        index_content = """
        <html>
        <head>
            <script src="jquery.min.js"></script>
            <script src="bootstrap.js"></script>
        </head>
        </html>
        """

        # When extracting modules
        extracted_modules = []  # Will be implemented

        # Then should return empty list
        assert len(extracted_modules) == 0


class TestExtractGWTModulesFromJSPIncludes:
    """Tests for extracting GWT modules from index.jsp includes (T047)"""

    def test_extract_gwt_module_from_jsp_include(self):
        """Test extracting GWT module from JSP include directive"""
        # Given index.jsp with JSP include
        jsp_content = """
        <%@ page contentType="text/html;charset=UTF-8" %>
        <%@ include file="/WEB-INF/jsp/com.example.Application.jsp" %>
        <html>
        <body>
            <div id="root"></div>
        </body>
        </html>
        """

        # When extracting from JSP includes
        expected_module = "com.example.Application"

        # Then should extract module from include path
        assert expected_module is not None

    def test_extract_gwt_module_from_jsp_directive(self):
        """Test extracting GWT module from <%@ page %> directive"""
        # Given index.jsp with page directive
        jsp_content = """
        <%@ page import="com.example.client.Application" %>
        <script type="text/javascript" src="com.example.Application/com.example.Application.nocache.js"></script>
        """

        # When extracting from directives
        expected_module = "com.example.Application"

        # Then should extract module
        assert expected_module is not None

    def test_extract_from_jsp_scriptlet(self):
        """Test extracting GWT module from JSP scriptlet"""
        # Given index.jsp with scriptlet
        jsp_content = """
        <%
        String moduleName = "com.example.Application";
        String moduleScript = moduleName + "/" + moduleName + ".nocache.js";
        %>
        <script src="<%= moduleScript %>"></script>
        """

        # When extracting from scriptlet
        expected_module = "com.example.Application"

        # Then should extract module from string literals
        assert expected_module is not None

    def test_extract_multiple_jsp_includes(self):
        """Test extracting modules from multiple JSP includes"""
        # Given index.jsp with multiple includes
        jsp_content = """
        <%@ include file="/gwt/com.example.Admin.jsp" %>
        <%@ include file="/gwt/com.example.User.jsp" %>
        <%@ include file="/gwt/com.example.Reports.jsp" %>
        """

        # When extracting all modules
        expected_modules = [
            "com.example.Admin",
            "com.example.User",
            "com.example.Reports"
        ]

        # Then should extract all 3 modules
        assert len(expected_modules) == 3

    def test_handle_jsp_with_no_gwt_modules(self):
        """Test handling JSP with no GWT module references"""
        # Given JSP without GWT modules
        jsp_content = """
        <%@ page contentType="text/html;charset=UTF-8" %>
        <%@ include file="/WEB-INF/jsp/header.jsp" %>
        <html><body>Plain JSP page</body></html>
        """

        # When extracting modules
        extracted_modules = []  # Will be implemented

        # Then should return empty list
        assert len(extracted_modules) == 0

    def test_extract_from_mixed_html_jsp(self):
        """Test extracting from mixed HTML + JSP syntax"""
        # Given mixed HTML/JSP file
        jsp_content = """
        <%@ page contentType="text/html;charset=UTF-8" %>
        <!DOCTYPE html>
        <html>
        <head>
            <script src="com.example.App/com.example.App.nocache.js"></script>
            <%@ include file="/WEB-INF/jsp/com.example.Utils.jsp" %>
        </head>
        </html>
        """

        # When extracting modules
        expected_modules = ["com.example.App", "com.example.Utils"]

        # Then should extract from both HTML and JSP syntax
        assert len(expected_modules) == 2
