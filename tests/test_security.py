from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_unauthenticated_denied():
    assert client.get('/documents').status_code == 401

def test_viewer_can_read():
    assert client.get('/documents', headers={'Authorization': 'Bearer demo-viewer-token'}).status_code == 200

def test_viewer_cannot_write():
    assert client.post('/documents', json={'title': 'blocked'}, headers={'Authorization': 'Bearer demo-viewer-token'}).status_code == 403

def test_admin_can_write():
    assert client.post('/documents', json={'title': 'approved'}, headers={'Authorization': 'Bearer demo-admin-token'}).status_code == 201

def test_invalid_token_denied():
    assert client.get('/documents', headers={'Authorization': 'Bearer invalid'}).status_code == 401
