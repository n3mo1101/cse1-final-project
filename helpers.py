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


def validate_data(data, is_update=False):
    # Validate product data according to business rules.
    if not is_update:
        if 'name' not in data or not data['name'].strip():
            return False, "Name is required and cannot be empty"
        if 'price' not in data:
            return False, "Price is required"
    
    if 'name' in data:
        if not isinstance(data['name'], str):
            return False, "Name must be a string"
        if not data['name'].strip():
            return False, "Name cannot be empty"
        if len(data['name']) > 45:
            return False, "Name must not exceed 45 characters"
    
    if 'description' in data and data['description'] is not None:
        if not isinstance(data['description'], str):
            return False, "Description must be a string"
        if len(data['description']) > 100:
            return False, "Description must not exceed 100 characters"
    
    if 'price' in data:
        try:
            price = float(data['price'])
            if price <= 0:
                return False, "Price must be greater than 0"
        except (ValueError, TypeError):
            return False, "Price must be a valid number"
    
    if 'stocks' in data and data['stocks'] is not None:
        try:
            stocks = int(data['stocks'])
            if stocks < 0:
                return False, "Stocks cannot be negative"
        except (ValueError, TypeError):
            return False, "Stocks must be a valid integer"
    
    return True, None
