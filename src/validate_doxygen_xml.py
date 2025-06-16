import os
import sys
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

def validate_doxygen_xml(xml_dir):
    """Validate Doxygen XML structure and content."""
    index_xml = os.path.join(xml_dir, 'index.xml')
    if not os.path.exists(index_xml):
        raise FileNotFoundError(f"index.xml not found in {xml_dir}")
    tree = ET.parse(index_xml)
    root = tree.getroot()
    compounds = root.findall('.//compound')
    expected_kinds = ['class', 'namespace']
    found_kinds = {}
    missing_kinds = []
    for kind in expected_kinds:
        found = [c for c in compounds if c.get('kind') == kind]
        found_kinds[kind] = found
        if not found:
            missing_kinds.append(kind)
    report = {
        'total_compounds': len(compounds),
        'found_kinds': {k: len(v) for k, v in found_kinds.items()},
        'missing_kinds': missing_kinds,
    }
    return report

def main():
    load_dotenv()
    xml_dir = os.getenv('XML_INPUT_DIR')
    if len(sys.argv) > 1:
        xml_dir = sys.argv[1]
    if not xml_dir:
        print("Error: XML_INPUT_DIR environment variable or CLI argument required.")
        sys.exit(1)
    report = validate_doxygen_xml(xml_dir)
    print("Validation Report:")
    print(f"Total compounds: {report['total_compounds']}")
    print("Found kinds:")
    for kind, count in report['found_kinds'].items():
        print(f"  {kind}: {count}")
    if report['missing_kinds']:
        print("Missing kinds:")
        for kind in report['missing_kinds']:
            print(f"  {kind}")
    else:
        print("All expected kinds found.")

if __name__ == "__main__":
    main() 