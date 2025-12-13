"""
Unit tests for language-specific parsers.

Tests Java, JSP, XML, and SQL parsers for entity extraction and classification.

NOTE: These tests should FAIL initially (TDD approach).
"""

import pytest
from pathlib import Path
from typing import List, Dict

from codeindex.parsers.java_parser import (
    JavaParser,
    extract_package,
    extract_imports,
    extract_classes,
    extract_methods,
    extract_annotations,
)
from codeindex.parsers.jsp_parser import (
    JSPParser,
    extract_form_fields,
    extract_taglibs,
    extract_controller_references,
    extract_embedded_java,
)
from codeindex.parsers.xml_parser import (
    XMLParser,
    classify_xml_type,
    extract_spring_beans,
    extract_hibernate_mappings,
    extract_gwt_modules,
)
from codeindex.parsers.sql_parser import (
    SQLParser,
    extract_tables,
    extract_columns,
    classify_sql_type,
    is_ddl,
    is_dml,
)


# ==============================================================================
# Java Parser Tests (T050)
# ==============================================================================

@pytest.fixture
def sample_java_file():
    """Path to sample Java file."""
    return Path(__file__).parent.parent / "fixtures" / "sample_java" / "SampleClass.java"


@pytest.fixture
def sample_java_content(sample_java_file):
    """Content of sample Java file."""
    with open(sample_java_file, 'r') as f:
        return f.read()


@pytest.fixture
def java_parser():
    """JavaParser instance."""
    return JavaParser()


class TestJavaParser:
    """Test Java source code parsing."""

    def test_extract_package(self, sample_java_content):
        """Test extraction of package declaration."""
        package = extract_package(sample_java_content)

        assert package is not None
        assert "example" in package or "test" in package

    def test_extract_imports(self, sample_java_content):
        """Test extraction of import statements."""
        imports = extract_imports(sample_java_content)

        assert isinstance(imports, list)
        assert len(imports) > 0
        assert any("java.util" in imp for imp in imports)

    def test_extract_classes(self, sample_java_content):
        """Test extraction of class definitions."""
        classes = extract_classes(sample_java_content)

        assert isinstance(classes, list)
        assert len(classes) > 0
        assert any("SampleClass" in cls for cls in classes)

    def test_extract_methods(self, sample_java_content):
        """Test extraction of method signatures."""
        methods = extract_methods(sample_java_content)

        assert isinstance(methods, list)
        assert len(methods) > 0
        # Should find methods like greet, increment, getCount
        method_names = [m.get("name", "") for m in methods]
        assert any("greet" in name for name in method_names)

    def test_extract_annotations(self):
        """Test extraction of Java annotations."""
        annotated_code = """
        @Entity
        @Table(name = "users")
        public class User {
            @Id
            @GeneratedValue
            private Long id;
        }
        """

        annotations = extract_annotations(annotated_code)

        assert len(annotations) >= 2
        assert any("Entity" in ann for ann in annotations)
        assert any("Table" in ann for ann in annotations)

    def test_parse_interface(self):
        """Test parsing Java interface."""
        interface_code = """
        package com.example;

        public interface UserService {
            User findById(Long id);
            void save(User user);
        }
        """

        parser = JavaParser()
        result = parser.parse(interface_code)

        assert result is not None
        assert result.get("package") == "com.example"
        assert "interface" in str(result).lower()

    def test_parse_enum(self):
        """Test parsing Java enum."""
        enum_code = """
        package com.example;

        public enum Status {
            ACTIVE, INACTIVE, PENDING
        }
        """

        parser = JavaParser()
        result = parser.parse(enum_code)

        assert result is not None
        assert "Status" in str(result)

    def test_extract_fields(self):
        """Test extraction of class fields."""
        code = """
        public class User {
            private String name;
            private int age;
            public static final int MAX_AGE = 120;
        }
        """

        parser = JavaParser()
        result = parser.parse(code)

        fields = result.get("fields", [])
        assert len(fields) >= 2
        field_names = [f.get("name", "") for f in fields]
        assert "name" in field_names
        assert "age" in field_names

    def test_parse_nested_classes(self):
        """Test parsing nested/inner classes."""
        code = """
        public class Outer {
            private class Inner {
                void method() {}
            }
        }
        """

        parser = JavaParser()
        result = parser.parse(code)

        assert result is not None
        # Should detect both outer and inner classes
        classes = result.get("classes", [])
        assert len(classes) >= 1


# ==============================================================================
# JSP Parser Tests (T051)
# ==============================================================================

@pytest.fixture
def sample_jsp_file():
    """Path to sample JSP file."""
    return Path(__file__).parent.parent / "fixtures" / "sample_jsp" / "SampleForm.jsp"


@pytest.fixture
def sample_jsp_content(sample_jsp_file):
    """Content of sample JSP file."""
    if sample_jsp_file.exists():
        with open(sample_jsp_file, 'r') as f:
            return f.read()
    return """
    <%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
    <form action="submitUser" method="post">
        <input type="text" name="username" />
        <input type="email" name="email" />
        <input type="password" name="password" />
        <button type="submit">Submit</button>
    </form>
    """


@pytest.fixture
def jsp_parser():
    """JSPParser instance."""
    return JSPParser()


class TestJSPParser:
    """Test JSP template parsing."""

    def test_extract_form_fields(self, sample_jsp_content):
        """Test extraction of form input fields."""
        fields = extract_form_fields(sample_jsp_content)

        assert isinstance(fields, list)
        assert len(fields) > 0
        # Should find username, email, password fields
        field_names = [f.get("name", "") for f in fields]
        assert "username" in field_names or "email" in field_names

    def test_extract_taglibs(self, sample_jsp_content):
        """Test extraction of JSP taglib declarations."""
        taglibs = extract_taglibs(sample_jsp_content)

        assert isinstance(taglibs, list)
        # JSTL core taglib should be present
        assert any("jstl" in tl.lower() for tl in taglibs)

    def test_extract_controller_references(self, sample_jsp_content):
        """Test extraction of controller/action references."""
        controllers = extract_controller_references(sample_jsp_content)

        assert isinstance(controllers, list)
        # Should find form action targets
        if "action=" in sample_jsp_content:
            assert len(controllers) > 0

    def test_extract_embedded_java(self):
        """Test extraction of embedded Java scriptlets."""
        jsp_with_scriptlet = """
        <%@ page language="java" %>
        <%
            String message = "Hello";
            out.println(message);
        %>
        <%= message %>
        """

        java_code = extract_embedded_java(jsp_with_scriptlet)

        assert isinstance(java_code, list)
        assert len(java_code) > 0
        # Should find the scriptlet code
        assert any("String message" in code for code in java_code)

    def test_parse_custom_tags(self):
        """Test parsing custom JSP tags."""
        jsp_with_custom = """
        <%@ taglib uri="/WEB-INF/custom.tld" prefix="custom" %>
        <custom:widget name="myWidget" />
        """

        parser = JSPParser()
        result = parser.parse(jsp_with_custom)

        taglibs = result.get("taglibs", [])
        assert any("custom" in tl for tl in taglibs)

    def test_parse_el_expressions(self):
        """Test parsing JSP EL expressions."""
        jsp_with_el = """
        <p>User: ${user.name}</p>
        <p>Age: ${user.age}</p>
        <c:if test="${user.active}">Active</c:if>
        """

        parser = JSPParser()
        result = parser.parse(jsp_with_el)

        el_expressions = result.get("el_expressions", [])
        assert len(el_expressions) >= 2
        assert any("user.name" in expr for expr in el_expressions)


# ==============================================================================
# XML Parser Tests (T052)
# ==============================================================================

@pytest.fixture
def spring_config_file():
    """Path to Spring config XML."""
    return Path(__file__).parent.parent / "fixtures" / "sample_xml" / "spring-config.xml"


@pytest.fixture
def mybatis_mapper_file():
    """Path to MyBatis mapper XML."""
    return Path(__file__).parent.parent / "fixtures" / "sample_xml" / "mybatis-mapper.xml"


@pytest.fixture
def xml_parser():
    """XMLParser instance."""
    return XMLParser()


class TestXMLParser:
    """Test XML configuration file parsing."""

    def test_classify_spring_config(self, spring_config_file):
        """Test classification of Spring configuration."""
        if spring_config_file.exists():
            with open(spring_config_file, 'r') as f:
                content = f.read()

            xml_type = classify_xml_type(content)
            assert "spring" in xml_type.lower()

    def test_classify_hibernate_mapping(self):
        """Test classification of Hibernate mapping XML."""
        hibernate_xml = """
        <!DOCTYPE hibernate-mapping PUBLIC
            "-//Hibernate/Hibernate Mapping DTD 3.0//EN"
            "http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">
        <hibernate-mapping>
            <class name="User" table="users">
                <id name="id" column="id"/>
            </class>
        </hibernate-mapping>
        """

        xml_type = classify_xml_type(hibernate_xml)
        assert "hibernate" in xml_type.lower()

    def test_classify_gwt_module(self):
        """Test classification of GWT module XML."""
        gwt_xml = """
        <module>
            <inherits name='com.google.gwt.user.User'/>
            <entry-point class='com.example.client.MyApp'/>
        </module>
        """

        xml_type = classify_xml_type(gwt_xml)
        assert "gwt" in xml_type.lower()

    def test_extract_spring_beans(self, spring_config_file):
        """Test extraction of Spring bean definitions."""
        if spring_config_file.exists():
            with open(spring_config_file, 'r') as f:
                content = f.read()

            beans = extract_spring_beans(content)
            assert isinstance(beans, list)

    def test_extract_hibernate_mappings(self):
        """Test extraction of Hibernate entity mappings."""
        hibernate_xml = """
        <hibernate-mapping>
            <class name="User" table="users">
                <id name="id"/>
                <property name="name"/>
            </class>
        </hibernate-mapping>
        """

        mappings = extract_hibernate_mappings(hibernate_xml)
        assert isinstance(mappings, list)
        assert len(mappings) > 0

    def test_parse_mybatis_mapper(self, mybatis_mapper_file):
        """Test parsing MyBatis/iBATIS mapper."""
        if mybatis_mapper_file.exists():
            parser = XMLParser()
            with open(mybatis_mapper_file, 'r') as f:
                content = f.read()

            result = parser.parse(content)
            assert result is not None
            assert "mapper" in result.get("type", "").lower() or "mybatis" in result.get("type", "").lower()

    def test_parse_web_xml(self):
        """Test parsing web.xml deployment descriptor."""
        web_xml = """
        <web-app>
            <servlet>
                <servlet-name>dispatcher</servlet-name>
                <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
            </servlet>
        </web-app>
        """

        parser = XMLParser()
        result = parser.parse(web_xml)

        assert result is not None
        servlets = result.get("servlets", [])
        assert len(servlets) > 0


# ==============================================================================
# SQL Parser Tests (T053)
# ==============================================================================

@pytest.fixture
def sql_parser():
    """SQLParser instance."""
    return SQLParser()


class TestSQLParser:
    """Test SQL file parsing."""

    def test_extract_tables_from_ddl(self):
        """Test extraction of table names from DDL."""
        ddl = """
        CREATE TABLE users (
            id BIGINT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE
        );

        CREATE TABLE orders (
            id BIGINT PRIMARY KEY,
            user_id BIGINT REFERENCES users(id)
        );
        """

        tables = extract_tables(ddl)
        assert "users" in tables
        assert "orders" in tables

    def test_extract_columns(self):
        """Test extraction of column definitions."""
        ddl = """
        CREATE TABLE users (
            id BIGINT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        columns = extract_columns(ddl, "users")
        assert len(columns) >= 3
        column_names = [c.get("name", "") for c in columns]
        assert "id" in column_names
        assert "username" in column_names
        assert "email" in column_names

    def test_classify_ddl(self):
        """Test classification of DDL statements."""
        ddl = "CREATE TABLE test (id INT);"
        assert is_ddl(ddl)
        assert classify_sql_type(ddl) == "ddl"

    def test_classify_dml(self):
        """Test classification of DML statements."""
        dml = "SELECT * FROM users WHERE id = 1;"
        assert is_dml(dml)
        assert classify_sql_type(dml) == "dml"

    def test_parse_create_table(self, sql_parser):
        """Test parsing CREATE TABLE statement."""
        ddl = """
        CREATE TABLE users (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_username (username),
            INDEX idx_email (email)
        );
        """

        result = sql_parser.parse(ddl)

        assert result is not None
        assert "users" in result.get("tables", [])
        columns = result.get("columns", [])
        assert len(columns) >= 4

    def test_parse_alter_table(self, sql_parser):
        """Test parsing ALTER TABLE statement."""
        alter = """
        ALTER TABLE users
        ADD COLUMN last_login TIMESTAMP,
        ADD INDEX idx_last_login (last_login);
        """

        result = sql_parser.parse(alter)
        assert "users" in result.get("tables", [])

    def test_parse_select_query(self, sql_parser):
        """Test parsing SELECT query."""
        select = """
        SELECT u.username, u.email, o.order_date
        FROM users u
        JOIN orders o ON u.id = o.user_id
        WHERE u.active = true
        ORDER BY o.order_date DESC;
        """

        result = sql_parser.parse(select)

        assert result is not None
        tables = result.get("tables", [])
        assert "users" in tables
        assert "orders" in tables

    def test_parse_insert_statement(self, sql_parser):
        """Test parsing INSERT statement."""
        insert = """
        INSERT INTO users (username, email, password_hash)
        VALUES ('testuser', 'test@example.com', 'hashed_password');
        """

        result = sql_parser.parse(insert)

        assert result is not None
        assert "users" in result.get("tables", [])
        assert result.get("operation", "").upper() == "INSERT"

    def test_parse_foreign_keys(self):
        """Test extraction of foreign key constraints."""
        ddl = """
        CREATE TABLE orders (
            id BIGINT PRIMARY KEY,
            user_id BIGINT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """

        parser = SQLParser()
        result = parser.parse(ddl)

        foreign_keys = result.get("foreign_keys", [])
        assert len(foreign_keys) > 0
        assert any("users" in fk.get("references", "") for fk in foreign_keys)
