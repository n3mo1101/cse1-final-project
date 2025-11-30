import xml.etree.ElementTree as ET
from flask import request, jsonify

def dict_to_xml(data, root_name="response"):
    # Convert dictionary or list to XML format.
    root = ET.Element(root_name)
    
    if isinstance(data, list):
        for item in data:
            item_elem = ET.SubElement(root, "item")
            for key, value in item.items():
                child = ET.SubElement(item_elem, str(key))
                child.text = str(value)
    elif isinstance(data, dict):
        for key, value in data.items():
            child = ET.SubElement(root, str(key))
            child.text = str(value)
    
    return ET.tostring(root, encoding='unicode')


def format_response(app, data, status_code=200):
    # Format response as JSON or XML based on query parameter.
    response_format = request.args.get('format', 'json').lower()
    
    if response_format == 'xml':
        xml_data = dict_to_xml(data)
        return app.response_class(
            response=xml_data,
            status=status_code,
            mimetype='application/xml'
        )
    else:
        return jsonify(data), status_code

