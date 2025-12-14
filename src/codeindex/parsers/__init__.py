"""
Parsers for various file types.

Provides structural parsing for:
- Java source files
- JSP files
- XML configuration files
- SQL scripts
"""

from .java_parser import (
    JavaParser,
    parse_java_file,
    extract_package,
    extract_imports,
    extract_classes,
    extract_interfaces,
    extract_methods,
    extract_annotations,
    JavaElement,
    JavaMethod,
    JavaClass,
)

from .jsp_parser import (
    JSPParser,
    parse_jsp_file,
    extract_directives,
    extract_taglibs,
    extract_scriptlets,
    extract_expressions,
    extract_declarations,
    extract_jsp_tags,
    extract_el_expressions,
)

from .xml_parser import (
    XMLParser,
    parse_xml_file,
    extract_root_element,
    extract_namespaces,
    extract_beans,
    extract_elements_by_tag,
)

from .sql_parser import (
    SQLParser,
    parse_sql_file,
    extract_statements,
    extract_tables,
    extract_statement_types,
)

__all__ = [
    # Java parser
    'JavaParser',
    'parse_java_file',
    'extract_package',
    'extract_imports',
    'extract_classes',
    'extract_interfaces',
    'extract_methods',
    'extract_annotations',
    'JavaElement',
    'JavaMethod',
    'JavaClass',
    # JSP parser
    'JSPParser',
    'parse_jsp_file',
    'extract_directives',
    'extract_taglibs',
    'extract_scriptlets',
    'extract_expressions',
    'extract_declarations',
    'extract_jsp_tags',
    'extract_el_expressions',
    # XML parser
    'XMLParser',
    'parse_xml_file',
    'extract_root_element',
    'extract_namespaces',
    'extract_beans',
    'extract_elements_by_tag',
    # SQL parser
    'SQLParser',
    'parse_sql_file',
    'extract_statements',
    'extract_tables',
    'extract_statement_types',
]
