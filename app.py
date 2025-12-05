from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from helpers import format_response, validate_data, generate_token, authenticate_user, token_required


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
            "GET /api/products/search?name=keyword": "Search products by name",
            "POST /api/products": "Create new product",
            "PUT /api/products/": "Update product",
            "DELETE /api/products/": "Delete product"
        }
    })


@app.route('/api/auth/login', methods=['POST'])
def login():
    # Authenticate user and return JWT token.
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No credentials provided"}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    if authenticate_user(username, password):
        token = generate_token(username)
        
        return jsonify({
            "message": "Login successful",
            "token": token,
            "expires_in": "1 hour"
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route('/api/products', methods=['GET'])
def get_products():
    # Get all products.
    connection = get_db_connection()
    if not connection:
        return format_response(app, {"error": "Database connection failed"}, 500)
    
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
        return format_response(app, products)
    except Error as e:
        return format_response(app, {"error": str(e)}, 500)


@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    # Get a single product by ID.
    connection = get_db_connection()
    if not connection:
        return format_response(app, {"error": "Database connection failed"}, 500)
    
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
        
        return format_response(app, product)
    except Error as e:
        return format_response(app, {"error": str(e)}, 500)


@app.route('/api/products/search', methods=['GET'])
def search_products():
    # Search for products by name in query.
    search_name = request.args.get('name', '').strip()
    
    if not search_name:
        return format_response(app, {"error": "Search parameter 'name' is required"}, 400)
    
    connection = get_db_connection()
    if not connection:
        return format_response(app, {"error": "Database connection failed"}, 500)
    
    try:
        cursor = connection.cursor()
        search_pattern = f"%{search_name.lower()}%"
        cursor.execute(
            "SELECT * FROM products WHERE LOWER(name) LIKE %s",
            (search_pattern,)
        )
        
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
        
        return format_response(app, products)
    except Error as e:
        return format_response(app, {"error": str(e)}, 500)


@app.route('/api/products', methods=['POST'])
@token_required
def create_product():
    # Create a new product.
    connection = get_db_connection()
    if not connection:
        return format_response(app, {"error": "Database connection failed"}, 500)
    
    try:
        data = request.get_json()
        
        if not data:
            return format_response(app, {"error": "No data provided"}, 400)
        
        is_valid, error_message = validate_data(data)
        if not is_valid:
            return format_response(app, {"error": error_message}, 400)
        
        name = data['name'].strip()
        description = data.get('description', None)
        price = float(data['price'])
        stocks = int(data.get('stocks', 0))
        
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO products (name, description, price, stocks) VALUES (%s, %s, %s, %s)",
            (name, description, price, stocks)
        )
        connection.commit()
        
        new_id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        new_product = {
            'id': new_id,
            'name': name,
            'description': description,
            'price': price,
            'stocks': stocks,
            'message': 'Product created successfully'
        }
        
        return format_response(app, new_product, 201)
    except Error as e:
        return format_response(app, {"error": str(e)}, 500)


@app.route('/api/products/<int:id>', methods=['PUT'])
@token_required
def update_product(id):
    # Update an existing product.
    connection = get_db_connection()
    if not connection:
        return format_response(app, {"error": "Database connection failed"}, 500)
    
    try:
        data = request.get_json()
        
        if not data:
            return format_response(app, {"error": "No data provided"}, 400)

        is_valid, error_message = validate_data(data, is_update=True)
        if not is_valid:
            connection.close()
            return format_response(app, {"error": error_message}, 400)
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        existing_product = cursor.fetchone()
        
        if existing_product is None:
            cursor.close()
            connection.close()
            return format_response(app, {"error": "Product not found"}, 404)

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
            return format_response(app, {"error": "No valid fields to update"}, 400)
        
        update_values.append(id)
        update_query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(update_query, tuple(update_values))
        connection.commit()
        
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        
        updated_product = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'price': float(row[3]),
            'stocks': row[4],
            'message': 'Product updated successfully'
        }
        
        return format_response(app, updated_product)
    except Error as e:
        return format_response(app, {"error": str(e)}, 500)


@app.route('/api/products/<int:id>', methods=['DELETE'])
@token_required
def delete_product(id):
    # Delete a product by ID.
    connection = get_db_connection()
    if not connection:
        return format_response(app, {"error": "Database connection failed"}, 500)

    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        existing_product = cursor.fetchone()
        
        if existing_product is None:
            cursor.close()
            connection.close()
            return format_response(app, {"error": "Product not found"}, 404)

        cursor.execute("DELETE FROM products WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        delete_product = {
            "message": "Product deleted successfully",
            "id": id
        }
        
        return format_response(app, delete_product)
    except Error as e:
        return format_response(app, {"error": str(e)}, 500)


if __name__ == "__main__":
    app.run(debug=True)
