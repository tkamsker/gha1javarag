import os
import xml.etree.ElementTree as ET
from pathlib import Path
from dotenv import load_dotenv

def inspect_doxygen_xml(xml_dir):
    """Inspect Doxygen XML files to verify structure and content."""
    print("\nInspecting Doxygen XML files...")
    
    # Check if directory exists
    if not os.path.exists(xml_dir):
        print(f"Error: Directory {xml_dir} does not exist")
        return
    
    # Find index.xml
    index_xml = os.path.join(xml_dir, 'index.xml')
    if not os.path.exists(index_xml):
        print(f"Error: index.xml not found in {xml_dir}")
        return
    
    # Parse index.xml
    try:
        tree = ET.parse(index_xml)
        root = tree.getroot()
        
        # Check compound elements
        compounds = root.findall('.//compound')
        print(f"\nFound {len(compounds)} compound elements")
        
        # Analyze compound types
        compound_types = {}
        for compound in compounds:
            kind = compound.get('kind')
            name = compound.find('name')
            name_text = name.text if name is not None else 'None'
            compound_types[kind] = compound_types.get(kind, 0) + 1
            print(f"\nCompound: {name_text} (kind: {kind})")
            
            # Get detailed information
            refid = compound.get('refid')
            if refid:
                detail_file = os.path.join(xml_dir, f'{refid}.xml')
                if os.path.exists(detail_file):
                    try:
                        detail_tree = ET.parse(detail_file)
                        detail_root = detail_tree.getroot()
                        
                        # Get compound name
                        compound_name = detail_root.find('.//compoundname')
                        if compound_name is not None:
                            print(f"  Compound name: {compound_name.text}")
                        
                        # Get base classes
                        base_classes = detail_root.findall('.//basecompoundref')
                        if base_classes:
                            print("  Base classes:")
                            for base in base_classes:
                                print(f"    - {base.text}")
                        
                        # Get members
                        members = detail_root.findall('.//member')
                        if members:
                            print(f"  Members: {len(members)}")
                            for member in members[:5]:  # Show first 5 members
                                member_name = member.find('name')
                                if member_name is not None:
                                    print(f"    - {member_name.text}")
                    except Exception as e:
                        print(f"  Error parsing detail file: {e}")
        
        print("\nCompound type distribution:")
        for kind, count in compound_types.items():
            print(f"  {kind}: {count}")
            
    except Exception as e:
        print(f"Error parsing index.xml: {e}")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Get XML directory from environment variable
    xml_dir = os.getenv('XML_INPUT_DIR')
    if not xml_dir:
        print("Error: XML_INPUT_DIR environment variable not set")
        exit(1)
        
    print(f"Using XML directory: {xml_dir}")
    inspect_doxygen_xml(xml_dir) 