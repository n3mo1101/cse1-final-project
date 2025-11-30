from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'flask_api_db'
}


def get_db_connection():
    # Create and return a database connection.
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


@app.route('/')
def home():
    # Home endpoint with API information.
    return jsonify({
        "message": "CRUD API for Products",
        "version": "1.0",
        "endpoints": {
            "GET /api/products": "Get all products",
            "GET /api/products/": "Get product by ID",
            "POST /api/products": "Create new product",
            "PUT /api/products/": "Update product",
            "DELETE /api/products/": "Delete product"
        }
    })


@app.route('/api/products', methods=['GET'])
def get_products():
    # Get all products.
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        
        products = []
        for row in rows:
            product = {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': float(row[3]),
                'stocks': row[4]
            }
            products.append(product)
        
        cursor.close()
        connection.close()
        return jsonify(products)
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    # Get a single product by ID.
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        row = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if row is None:
            return jsonify({"error": "Product not found"}), 404
        
        product = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'price': float(row[3]),
            'stocks': row[4]
        }
        return jsonify(product)
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/products', methods=['POST'])
def create_product():
    # Create a new product.
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        name = data.get('name')
        description = data.get('description', None)
        price = data.get('price')
        stocks = data.get('stocks', 0)
        
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO products (name, description, price, stocks) VALUES (%s, %s, %s, %s)",
            (name, description, price, stocks)
        )
        connection.commit()
        
        new_id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return jsonify({
            'id': new_id,
            'name': name,
            'description': description,
            'price': price,
            'stocks': stocks,
            'message': 'Product created successfully'
        }), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    # Update an existing product.
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        existing_product = cursor.fetchone()
        
        if existing_product is None:
            cursor.close()
            connection.close()
            return jsonify({"error": "Product not found"}), 404
        
        update_fields = []
        update_values = []
        
        if 'name' in data:
            update_fields.append("name = %s")
            update_values.append(data['name'])
        if 'description' in data:
            update_fields.append("description = %s")
            update_values.append(data['description'])
        if 'price' in data:
            update_fields.append("price = %s")
            update_values.append(data['price'])
        if 'stocks' in data:
            update_fields.append("stocks = %s")
            update_values.append(data['stocks'])
        
        if not update_fields:
            cursor.close()
            connection.close()
            return jsonify({"error": "No valid fields to update"}), 400
        
        update_values.append(id)
        update_query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(update_query, tuple(update_values))
        connection.commit()
        
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return jsonify({
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'price': float(row[3]),
            'stocks': row[4],
            'message': 'Product updated successfully'
        })
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    # Delete a product by ID.
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        existing_product = cursor.fetchone()
        
        if existing_product is None:
            cursor.close()
            connection.close()
            return jsonify({"error": "Product not found"}), 404
        
        cursor.execute("DELETE FROM products WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            "message": "Product deleted successfully",
            "id": id
        })
    except Error as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
