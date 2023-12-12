import json
from app import app, search_recipes

def test_home_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_search_no_keyword():
    client = app.test_client()
    response = client.get('/search')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] is False
    assert 'No keyword provided' in data['message']

def test_search_with_keyword():
    client = app.test_client()
    response = client.get('/search?query=cake&page=1')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] is True
    assert 'data' in data
    assert isinstance(data['data'], list)

def test_search_recipes():
    # Assuming you have sample data in your test database
    result = search_recipes('cake', 0, 10)
    assert len(result) > 0
    assert isinstance(result[0], dict)
    assert 'title' in result[0]
    assert 'NER' in result[0]
    assert 'link' in result[0]

def test_pagination():
    client = app.test_client()
    
    # Assuming you have more than one page of results in your test database
    response = client.get('/search?query=cake&page=2')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] is True
    assert 'data' in data
    assert isinstance(data['data'], list)