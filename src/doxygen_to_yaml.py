import os
import sys
import xml.etree.ElementTree as ET
import yaml
from dotenv import load_dotenv

def parse_doxygen_xml(xml_dir):
    """Parse Doxygen XML and extract classes, namespaces, and members."""
    index_xml = os.path.join(xml_dir, 'index.xml')
    if not os.path.exists(index_xml):
        raise FileNotFoundError(f"index.xml not found in {xml_dir}")
    tree = ET.parse(index_xml)
    root = tree.getroot()
    compounds = root.findall('.//compound')
    result = []
    for compound in compounds:
        kind = compound.get('kind')
        name = compound.find('name')
        name_text = name.text if name is not None else None
        refid = compound.get('refid')
        entry = {
            'kind': kind,
            'name': name_text,
        }
        if refid:
            detail_file = os.path.join(xml_dir, f'{refid}.xml')
            if os.path.exists(detail_file):
                detail_tree = ET.parse(detail_file)
                detail_root = detail_tree.getroot()
                compound_name = detail_root.find('.//compoundname')
                if compound_name is not None:
                    entry['compound_name'] = compound_name.text
                # Base classes
                base_classes = [b.text for b in detail_root.findall('.//basecompoundref') if b.text]
                if base_classes:
                    entry['base_classes'] = base_classes
                # Members
                members = []
                for member in detail_root.findall('.//memberdef'):
                    member_kind = member.get('kind')
                    member_name = member.find('name')
                    member_entry = {
                        'kind': member_kind,
                        'name': member_name.text if member_name is not None else None,
                    }
                    # Brief description
                    brief = member.find('briefdescription')
                    if brief is not None:
                        brief_text = ''.join(brief.itertext()).strip()
                        if brief_text:
                            member_entry['brief'] = brief_text
                    # Detailed description
                    detailed = member.find('detaileddescription')
                    if detailed is not None:
                        detailed_text = ''.join(detailed.itertext()).strip()
                        if detailed_text:
                            member_entry['detailed'] = detailed_text
                    members.append(member_entry)
                if members:
                    entry['members'] = members
        result.append(entry)
    return result

def main():
    load_dotenv()
    xml_dir = os.getenv('XML_INPUT_DIR')
    if len(sys.argv) > 1:
        xml_dir = sys.argv[1]
    if not xml_dir:
        print("Error: XML_INPUT_DIR environment variable or CLI argument required.")
        sys.exit(1)
    data = parse_doxygen_xml(xml_dir)
    output_file = os.path.join(xml_dir, 'doxygen_output.yaml')
    with open(output_file, 'w') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)
    print(f"YAML output written to {output_file}")

if __name__ == "__main__":
    main() 