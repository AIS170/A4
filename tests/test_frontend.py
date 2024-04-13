import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_frontend_signup_html(client):
    response = client.get('/auth/signup', follow_redirects=True)
    assert response.status_code == 200

def test_frontend_login_html(client):
    response = client.get('/auth/login', follow_redirects=True)
    assert response.status_code == 200

# def test_frontend_login_html(client):
#     response = client.get('/mailbox/sending', follow_redirects=True)
#     assert response.status_code == 200

# def test_frontend_sending_html(client):
#     response = client.get('/mailbox/sending', follow_redirects=True)
#     assert response.status_code == 200