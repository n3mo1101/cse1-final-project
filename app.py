from flask import Flask, jsonify
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


if __name__ == "__main__":
    app.run(debug=True)
