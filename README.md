# CSE1 Final Project: Flask REST API Web Application.

A RESTful API built with Flask for managing product inventory with full CRUD operations, search functionality, and JWT authentication.

## 🧩 Project Overview

This API provides a complete backend solution for product management with the following features:

- **Full CRUD Operations**: Create, Read, Update, and Delete products
- **Search Functionality**: Search products by name (partial match, case-insensitive)
- **JWT Authentication**: Secure endpoints with token-based authentication
- **Dual Format Support**: Responses available in both JSON and XML formats
- **Data Validation**: Comprehensive input validation with clear error messages
- **Error Handling**: Proper HTTP status codes and error responses

## 🚀 Technologies Used

- **Backend Framework**: Flask 3.1.0
- **Database**: MySQL 8.0
- **Authentication**: PyJWT 2.8.0
- **Database Connector**: mysql-connector-python 9.1.0
- **Testing**: pytest

## 📁 Project Structure

```
flask_project/
├── app.py              # Main application with API routes
├── helpers.py          # Helper functions (formatting, validation, auth)
├── test.py            # Unit tests (pytest)
requirements.txt   # Python dependencies
products.sql       # Database schema and sample data
.gitignore         # Git ignore rules
README.md          # Documentation
```

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10 or higher
- MySQL Server 8.0 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/n3mo1101/cse1-final-project.git
cd cse1-final-project
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database

1. **Start MySQL Server** (ensure it's running)

2. **Create Database**:
```bash
mysql -u root -p
```

```sql
CREATE DATABASE flask_api_db;
USE flask_api_db;
```

3. **Import Sample Data**:
```bash
# Exit MySQL, then run:
mysql -u root -p flask_api_db < products.sql
```

Or import via MySQL Workbench:
- Server → Data Import → Import from Self-Contained File
- Select `products.sql`

4. **Verify Import**:
```sql
USE flask_api_db;
SELECT COUNT(*) FROM products;
-- Should return 20
```

### Step 5: Configure Database Connection

Update `app.py` with your MySQL credentials (lines 10-14):

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # Update this!
    'database': 'flask_api_db'
}
```

### Step 6: Run the Application

```bash
python app.py
```

The server will start at: `http://127.0.0.1:5000/`

You should see:
```
 * Running on http://127.0.0.1:5000/
 * Restarting with stat
 * Debugger is active!
```

## 🌐 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login` | Login and get JWT token | No |

### Products

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products` | Get all products | No |
| GET | `/api/products/<id>` | Get product by ID | No |
| GET | `/api/products/search?name=keyword` | Search products by name | No |
| POST | `/api/products` | Create new product | **Yes** |
| PUT | `/api/products/<id>` | Update product | **Yes** |
| DELETE | `/api/products/<id>` | Delete product | **Yes** |

### Response Formats

Add `?format=xml` to any endpoint to get XML response:
- JSON (default): `GET /api/products`
- XML: `GET /api/products?format=xml`

## 📖 Usage Examples

### 1. Authentication

**Login to Get Token**:
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Response**:
```json
{
  "message": "Login successful",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_in": "24 hours"
}
```

**Test Credentials**:
- Username: `admin`
- Password: `admin123`

### 2. Get All Products

**JSON Format**:
```bash
curl http://127.0.0.1:5000/api/products
```

**XML Format**:
```bash
curl http://127.0.0.1:5000/api/products?format=xml
```

**Response (JSON)**:
```json
[
  {
    "id": 1,
    "name": "Wireless Keyboard",
    "description": "Ergonomic wireless keyboard with numeric keypad",
    "price": 29.99,
    "stocks": 45
  },
  ...
]
```

### 3. Get Single Product

```bash
curl http://127.0.0.1:5000/api/products/1
```

**Response**:
```json
{
  "id": 1,
  "name": "Wireless Keyboard",
  "description": "Ergonomic wireless keyboard with numeric keypad",
  "price": 29.99,
  "stocks": 45
}
```

### 4. Search Products

```bash
# Search for "keyboard"
curl http://127.0.0.1:5000/api/products/search?name=keyboard

# Search with XML format
curl http://127.0.0.1:5000/api/products/search?name=mouse&format=xml
```

**Features**:
- Partial match: "key" finds "keyboard"
- Case-insensitive: "KEYBOARD" = "keyboard"

### 5. Create Product (Requires Authentication)

```bash
curl -X POST http://127.0.0.1:5000/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "name": "Mechanical Keyboard",
    "description": "RGB mechanical keyboard",
    "price": 129.99,
    "stocks": 25
  }'
```

**Response**:
```json
{
  "id": 21,
  "name": "Mechanical Keyboard",
  "description": "RGB mechanical keyboard",
  "price": 129.99,
  "stocks": 25,
  "message": "Product created successfully"
}
```

### 6. Update Product (Requires Authentication)

```bash
curl -X PUT http://127.0.0.1:5000/api/products/21 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "price": 149.99,
    "stocks": 15
  }'
```

**Note**: Partial updates are supported - only send fields you want to update.

### 7. Delete Product (Requires Authentication)

```bash
curl -X DELETE http://127.0.0.1:5000/api/products/21 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response**:
```json
{
  "message": "Product deleted successfully",
  "id": 21
}
```

## 🔒 Authentication

Protected endpoints (POST, PUT, DELETE) require JWT authentication.

### How to Use Authentication:

1. **Login** to get a token:
```bash
POST /api/auth/login
Body: {"username": "admin", "password": "admin123"}
```

2. **Use the token** in subsequent requests:
```bash
Authorization: Bearer <your_token_here>
```

3. **Token expires** after 24 hours - login again to get a new token.

### Example Workflow:

```bash
# Step 1: Login
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# Step 2: Use token to create product
curl -X POST http://127.0.0.1:5000/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"New Product","price":99.99}'
```

## ✅ Data Validation

The API validates all input data:

### Product Fields:

| Field | Required | Type | Validation |
|-------|----------|------|------------|
| `name` | Yes (POST) | String | Max 45 chars, non-empty |
| `description` | No | String | Max 100 chars |
| `price` | Yes (POST) | Float | Must be > 0 |
| `stocks` | No | Integer | Must be >= 0 (default: 0) |

### Validation Examples:

```bash
# ❌ Missing name - ERROR
{"price": 50.00}

# ❌ Negative price - ERROR
{"name": "Test", "price": -10.00}

# ❌ Name too long - ERROR
{"name": "A very long product name that exceeds forty-five characters", "price": 50.00}

# ✅ Valid product
{"name": "Test Product", "description": "A test", "price": 50.00, "stocks": 10}
```

## 📊 HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid token |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server-side error |

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest test.py -v

# Run specific test
pytest test.py::test_search_functionality -v

# Run with coverage
pytest test.py --cov=app --cov=helpers
```

**Test Coverage**:
- ✅ All CRUD operations
- ✅ Search functionality
- ✅ JWT authentication
- ✅ Data validation
- ✅ Error handling
- ✅ XML/JSON formatting

Expected output:
```
===================== 9 passed in 2.5s =====================
```

## 📝 Sample Data

The `products.sql` file includes 20 sample products:

- Electronics (keyboards, mice, webcam)
- Office supplies (notebooks, pens, organizers)
- Accessories (backpack, phone case, water bottle)

All products have:
- Name (e.g., "Wireless Keyboard")
- Description
- Price (ranging from $3.99 to $49.99)
- Stock quantity

## 🔧 Configuration

### Database Configuration

Located in `app.py` (lines 10-14):
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'flask_api_db'
}
```

### JWT Configuration

Located in `helpers.py` (lines 86-88):
```python
SECRET_KEY = "your-secret-key"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24
```

### Test User

Located in `helpers.py` (line 92):
```python
USERS = {
    "admin": "admin123"
}
```

## 🪲 Troubleshooting

### Issue: Port 5000 already in use

**Solution**:
```python
# In app.py, last line, change port:
app.run(debug=True, port=5001)
```

### Issue: JWT token expired

**Solution**: Login again to get a new token (tokens expire after 24 hours).

## 👨‍💻 Development

### Code Structure

**app.py**: Main application
- Routes and endpoint logic
- Database connection
- Request/response handling

**helpers.py**: Utility functions
- `format_response()` - JSON/XML formatting
- `validate_data()` - Input validation
- `generate_token()` - JWT token creation
- `verify_token()` - JWT token validation
- `token_required` - Authentication decorator

**test.py**: Test suite
- 9 comprehensive tests
- Covers all endpoints and edge cases

## 📧 Contact

For questions or support, please contact https://github.com/n3mo1101

---

**Last Updated**: December 2025  
**Version**: 1.0.0  
**Status**: ✅ Complete