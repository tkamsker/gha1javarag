import os
import sys
import logging
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("inspect_doxygen_tree")

load_dotenv()
xml_input_dir = os.getenv("XML_INPUT_DIR")

if not xml_input_dir:
    logger.error("XML_INPUT_DIR environment variable not set.")
    sys.exit(1)
if not os.path.isdir(xml_input_dir):
    logger.error(f"Doxygen XML directory not found: {xml_input_dir}")
    sys.exit(1)

index_path = os.path.join(xml_input_dir, "index.xml")
if not os.path.isfile(index_path):
    logger.error(f"index.xml not found in {xml_input_dir}")
    sys.exit(1)

visited = set()

def print_node(elem, depth=0):
    indent = "  " * depth
    tag = elem.tag
    attribs = " ".join([f"{k}='{v}'" for k, v in elem.attrib.items()])
    name = elem.findtext("name")
    kind = elem.attrib.get("kind", "")
    refid = elem.attrib.get("refid", "")
    print(f"{indent}<{tag} {attribs} name='{name}' kind='{kind}' refid='{refid}'>")
    for child in elem:
        print_node(child, depth + 1)

def inspect_xml_file(xml_file, depth=0):
    if xml_file in visited:
        return
    visited.add(xml_file)
    path = os.path.join(xml_input_dir, xml_file)
    if not os.path.isfile(path):
        print("  " * depth + f"[Missing file: {xml_file}]")
        return
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        print("  " * depth + f"Inspecting: {xml_file}")
        print_node(root, depth + 1)
        # For index.xml, follow <compound refid="..."> to other files
        if xml_file == "index.xml":
            for compound in root.findall("compound"):  # Doxygen index.xml
                refid = compound.attrib.get("refid")
                if refid:
                    inspect_xml_file(f"{refid}.xml", depth + 1)
    except Exception as e:
        print("  " * depth + f"[Error parsing {xml_file}: {e}]")

inspect_xml_file("index.xml") 