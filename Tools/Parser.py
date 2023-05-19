import os
import xml.etree.ElementTree as ET
import json

def parse_xml_files(directory):
    data = []
    for xml_file in os.listdir(directory):
        if xml_file.endswith('.xml'):
            tree = ET.parse(os.path.join(directory, xml_file))
            root = tree.getroot()

            image_data = {'filename': root.find('filename').text,
                          'size': (int(root.find('size')[0].text), int(root.find('size')[1].text)),  # width, height
                          'objects': []}
                          
            for obj in root.iter('object'):
                label = obj.find('name').text
                bbox = obj.find('bndbox')
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)
                image_data['objects'].append({'label': label, 'bbox': (xmin, ymin, xmax, ymax)})

            data.append(image_data)

    # Save the data to a JSON file in the same directory
    with open(os.path.join(directory, 'parsed_annotations.json'), 'w') as f:
        json.dump(data, f)

    return data

data = parse_xml_files('/Users/sebastianmacias/Pictures/Train/boutinela/Model2/Batch1/')
