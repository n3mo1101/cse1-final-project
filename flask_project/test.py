# To run tests: pytest test_app.py -v

import pytest
import json
from app import app

# ============= TEST CONFIGURATION =============

@pytest.fixture
def client():
    # Create test client for Flask application.
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_token(client):
    # Login and return JWT token for authenticated requests
    response = client.post(
        '/api/auth/login',
        data=json.dumps({'username': 'admin', 'password': 'admin123'}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    return data['token']


# ============= TEST 1: HOME & API INFO =============

def test_home_endpoint(client):
    # Test home endpoint returns API information.
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'message' in data
    assert 'endpoints' in data
    assert 'authentication' in data
    assert data['authentication']['test_username'] == 'admin'


# ============= TEST 2: PUBLIC GET ENDPOINTS =============

def test_public_get_endpoints(client):
    # Test GET all products (JSON)
    response = client.get('/api/products')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    products = json.loads(response.data)
    assert isinstance(products, list)
    assert len(products) > 0
    
    # Test GET all products (XML)
    response = client.get('/api/products?format=xml')
    assert response.status_code == 200
    assert 'application/xml' in response.content_type
    assert b'<response>' in response.data
    
    # Test GET single product (JSON)
    response = client.get('/api/products/1')
    assert response.status_code == 200
    product = json.loads(response.data)
    assert product['id'] == 1
    assert 'name' in product
    assert 'price' in product
    
    # Test GET single product (XML)
    response = client.get('/api/products/1?format=xml')
    assert response.status_code == 200
    assert 'application/xml' in response.content_type
    
    # Test GET non-existent product (404)
    response = client.get('/api/products/999999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


# ============= TEST 3: SEARCH FUNCTIONALITY =============

def test_search_functionality(client):
    # Test search with results (JSON)
    response = client.get('/api/products/search?name=keyboard')
    assert response.status_code == 200
    results = json.loads(response.data)
    assert isinstance(results, list)
    # At least one product should contain "keyboard"
    assert any('keyboard' in p['name'].lower() for p in results)
    
    # Test search case-insensitive
    response = client.get('/api/products/search?name=KEYBOARD')
    assert response.status_code == 200
    results_upper = json.loads(response.data)
    assert len(results_upper) > 0
    
    # Test search partial match
    response = client.get('/api/products/search?name=key')
    assert response.status_code == 200
    results_partial = json.loads(response.data)
    assert len(results_partial) > 0
    
    # Test search with XML format
    response = client.get('/api/products/search?name=mouse&format=xml')
    assert response.status_code == 200
    assert 'application/xml' in response.content_type
    assert b'<response>' in response.data
    
    # Test search with no results (should return empty array)
    response = client.get('/api/products/search?name=nonexistentproduct12345')
    assert response.status_code == 200
    results = json.loads(response.data)
    assert results == []
    
    # Test search without parameter (should error)
    response = client.get('/api/products/search')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


# ============= TEST 4: AUTHENTICATION FLOW =============

def test_authentication_flow(client):
    # Test successful login
    response = client.post(
        '/api/auth/login',
        data=json.dumps({'username': 'admin', 'password': 'admin123'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert 'message' in data
    assert 'expires_in' in data
    token = data['token']
    
    # Test login with wrong password
    response = client.post(
        '/api/auth/login',
        data=json.dumps({'username': 'admin', 'password': 'wrongpassword'}),
        content_type='application/json'
    )
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data
    
    # Test login with missing credentials
    response = client.post(
        '/api/auth/login',
        data=json.dumps({'username': 'admin'}),
        content_type='application/json'
    )
    assert response.status_code == 400
    
    # Test using valid token to create product
    response = client.post(
        '/api/products',
        data=json.dumps({'name': 'Auth Test Product', 'price': 49.99, 'stocks': 10}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    
    # Test with invalid token
    response = client.post(
        '/api/products',
        data=json.dumps({'name': 'Should Fail', 'price': 49.99}),
        content_type='application/json',
        headers={'Authorization': 'Bearer invalid_token_123'}
    )
    assert response.status_code == 401


# ============= TEST 5: PROTECTED ENDPOINTS (CRUD WITH AUTH) =============

def test_protected_crud_operations(client, auth_token):
    # CREATE: Create a new product with authentication
    create_data = {
        'name': 'CRUD Test Product',
        'description': 'Testing CRUD operations',
        'price': 79.99,
        'stocks': 25
    }
    
    response = client.post(
        '/api/products',
        data=json.dumps(create_data),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 201
    created = json.loads(response.data)
    assert 'id' in created
    assert created['name'] == create_data['name']
    product_id = created['id']
    
    # READ: Verify product was created (no auth required for GET)
    response = client.get(f'/api/products/{product_id}')
    assert response.status_code == 200
    product = json.loads(response.data)
    assert product['id'] == product_id
    assert product['name'] == create_data['name']
    
    # UPDATE: Update the product with authentication
    update_data = {
        'name': 'Updated CRUD Product',
        'price': 99.99
    }
    
    response = client.put(
        f'/api/products/{product_id}',
        data=json.dumps(update_data),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    updated = json.loads(response.data)
    assert updated['name'] == update_data['name']
    assert updated['price'] == update_data['price']
    assert updated['stocks'] == create_data['stocks']  # Unchanged field
    
    # DELETE: Delete the product with authentication
    response = client.delete(
        f'/api/products/{product_id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    deleted = json.loads(response.data)
    assert deleted['id'] == product_id
    
    # Verify deletion (should return 404)
    response = client.get(f'/api/products/{product_id}')
    assert response.status_code == 404


# ============= TEST 6: PROTECTED ROUTES WITHOUT AUTH =============

def test_protected_routes_require_authentication(client):
    # Test POST without token
    response = client.post(
        '/api/products',
        data=json.dumps({'name': 'Should Fail', 'price': 49.99}),
        content_type='application/json'
    )
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data
    assert 'token' in data['error'].lower()
    
    # Test PUT without token
    response = client.put(
        '/api/products/1',
        data=json.dumps({'price': 99.99}),
        content_type='application/json'
    )
    assert response.status_code == 401
    
    # Test DELETE without token
    response = client.delete('/api/products/1')
    assert response.status_code == 401


# ============= TEST 7: DATA VALIDATION =============

def test_data_validation(client, auth_token):
    # Test missing required field (name)
    response = client.post(
        '/api/products',
        data=json.dumps({'price': 50.00, 'stocks': 10}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'name' in data['error'].lower()
    
    # Test missing required field (price)
    response = client.post(
        '/api/products',
        data=json.dumps({'name': 'Test Product'}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'price' in data['error'].lower()
    
    # Test negative price
    response = client.post(
        '/api/products',
        data=json.dumps({'name': 'Test', 'price': -10.00}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'price' in data['error'].lower()
    
    # Test zero price
    response = client.post(
        '/api/products',
        data=json.dumps({'name': 'Test', 'price': 0}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    
    # Test negative stocks
    response = client.post(
        '/api/products',
        data=json.dumps({'name': 'Test', 'price': 50.00, 'stocks': -5}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'stocks' in data['error'].lower()
    
    # Test name too long (>45 chars)
    response = client.post(
        '/api/products',
        data=json.dumps({'name': 'A' * 50, 'price': 50.00}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'name' in data['error'].lower()
    
    # Test description too long (>100 chars)
    response = client.post(
        '/api/products',
        data=json.dumps({
            'name': 'Test',
            'description': 'D' * 110,
            'price': 50.00
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'description' in data['error'].lower()
    
    # Test empty name (whitespace only)
    response = client.post(
        '/api/products',
        data=json.dumps({'name': '   ', 'price': 50.00}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400


# ============= TEST 8: ERROR HANDLING & EDGE CASES =============

def test_error_handling_and_edge_cases(client, auth_token):
    # Test UPDATE on non-existent product
    response = client.put(
        '/api/products/999999',
        data=json.dumps({'price': 99.99}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    
    # Test DELETE on non-existent product
    response = client.delete(
        '/api/products/999999',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 404
    
    # Test POST with no data
    response = client.post(
        '/api/products',
        data=json.dumps({}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    
    # Test PUT with no data
    response = client.put(
        '/api/products/1',
        data=json.dumps({}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    
    # Test partial UPDATE (only price)
    response = client.put(
        '/api/products/1',
        data=json.dumps({'price': 35.99}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['price'] == 35.99
    # Name should remain unchanged
    assert 'name' in data
    
    # Test invalid price type
    response = client.post(
        '/api/products',
        data=json.dumps({'name': 'Test', 'price': 'not-a-number'}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400


# ============= TEST 9: XML/JSON FORMAT CONSISTENCY =============

def test_format_consistency(client):
    # Test GET all products - JSON
    json_response = client.get('/api/products')
    assert json_response.status_code == 200
    assert json_response.content_type == 'application/json'
    json_data = json.loads(json_response.data)
    assert isinstance(json_data, list)
    
    # # Test GET all products - XML
    xml_response = client.get('/api/products?format=xml')
    assert xml_response.status_code == 200
    assert 'application/xml' in xml_response.content_type
    assert b'<response>' in xml_response.data
    assert b'<item>' in xml_response.data
    
    # Test GET single product - both formats
    json_response = client.get('/api/products/1')
    assert json_response.content_type == 'application/json'
    
    xml_response = client.get('/api/products/1?format=xml')
    assert 'application/xml' in xml_response.content_type
    
    # Test Search - both formats
    json_response = client.get('/api/products/search?name=keyboard')
    assert json_response.content_type == 'application/json'
    
    xml_response = client.get('/api/products/search?name=keyboard&format=xml')
    assert 'application/xml' in xml_response.content_type

# =============================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])