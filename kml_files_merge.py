import xml.etree.ElementTree as ET
import os

def create_kml_folder():
    # Directory measurement variable:
    kml_folder_path = r'upload\kml';

    # Check if the 'kml' directory already exists:
    kml_existente = os.path.exists(kml_folder_path);

    # Creation of the 'kml' directory, if it does not exist:
    if not kml_existente:
        os.makedirs(kml_folder_path);
        print('- Kml folder created!');

def concatenate_kml_files(input_files, output_file):
    # Create the KML root element:
    kml_root = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")

    # Create the KML document element:
    document = ET.SubElement(kml_root, "Document");

    for kml_file in input_files:
        # Parse each input KML file:
        tree = ET.parse(kml_file);
        root = tree.getroot();

        # Iterate over the elements in each KML file and append them to the document:
        for element in root:
            document.append(element);

    # Create a new KML tree with the concatenated content:
    concatenated_kml_tree = ET.ElementTree(kml_root);

    # Write the concatenated KML to the output file:
    with open(output_file, "wb") as output:
        output.write(b'<?xml version="1.0" encoding="UTF-8"?>\n');
        concatenated_kml_tree.write(output, encoding="utf-8");
