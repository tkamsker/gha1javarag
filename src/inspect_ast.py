import os
import sys
import logging
from dotenv import load_dotenv
from doxygen_parser import DoxygenParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("inspect_ast")

load_dotenv()
xml_input_dir = os.getenv("XML_INPUT_DIR")

if not xml_input_dir:
    logger.error("XML_INPUT_DIR environment variable not set.")
    sys.exit(1)
if not os.path.isdir(xml_input_dir):
    logger.error(f"Doxygen XML directory not found: {xml_input_dir}")
    sys.exit(1)

parser = DoxygenParser(xml_input_dir)
ast_data = parser.get_ast_data()

print("\n--- AST Inspection ---\n")

# Classes
print(f"Classes ({len(ast_data.get('classes', []))}):")
for i, cls in enumerate(ast_data.get('classes', [])):
    print(f"  [{i}] Name: {cls.get('name')} | Brief: {cls.get('brief', '')[:40]}...")
    if not cls.get('name'):
        print("    -> WARNING: Missing class name!")
    if 'methods' in cls:
        for j, m in enumerate(cls['methods']):
            print(f"      Method [{j}]: {m.get('name')} | Brief: {m.get('brief', '')[:40]}...")
            if not m.get('name'):
                print("        -> WARNING: Missing method name!")
print()

# Namespaces
print(f"Namespaces ({len(ast_data.get('namespaces', []))}):")
for i, ns in enumerate(ast_data.get('namespaces', [])):
    print(f"  [{i}] Name: {ns.get('name')} | Brief: {ns.get('brief', '')[:40]}...")
    if not ns.get('name'):
        print("    -> WARNING: Missing namespace name!")
    if 'classes' in ns:
        for j, c in enumerate(ns['classes']):
            print(f"      Class [{j}]: {c.get('name')}")
            if not c.get('name'):
                print("        -> WARNING: Missing class name in namespace!")
    if 'functions' in ns:
        for j, f in enumerate(ns['functions']):
            print(f"      Function [{j}]: {f.get('name')} | Brief: {f.get('brief', '')[:40]}...")
            if not f.get('name'):
                print("        -> WARNING: Missing function name in namespace!")
print("\n--- End of AST Inspection ---\n") 