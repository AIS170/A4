import pytest
import requests

BASE_URL = "http://localhost:5000"

# Define valid test data
valid_registration_data1 = {
    "firstName": "First",
    "lastName": "User",
    "email": "user@example.com",
    "password": "val1dPassword",
    "confirmPassword": "val1dPassword"
}

valid_registration_data2 = {
    "firstName": "Second",
    "lastName": "User",
    "email": "user2@example.com",
    "password": "val1dPassword",
    "confirmPassword": "val1dPassword"
}

valid_login_data = {
    "email": "user@example.com",
    "password": "val1dPassword",
}

@pytest.fixture
def session():
    return requests.Session()

#Test successful user registration
def test_signup_success(session):
    session.delete(f"{BASE_URL}/clear")
    response = session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    assert response.status_code == 200

# Test two successful user registrations
def test_signup_success_two_users(session):
    session.delete(f"{BASE_URL}/clear")
    response1 = session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    assert response1.status_code == 200
    response2 = session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
    assert response2.status_code == 200

# # Test user registration with same email
# def test_signup_email_in_use(session):
#     session.delete(f"{BASE_URL}/clear")
#     response1 = session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
#     assert response1.status_code == 200
#     assert 'userId' in response1.json()
#     response2 = session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
#     assert response2.status_code == 400

# Test user registration with non matching passwords
def test_signup_password_not_matching(session):
    session.delete(f"{BASE_URL}/clear")
    invalid_data = valid_registration_data1.copy()
    invalid_data['confirmPassword'] = 'val0dPassword'
    response = session.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Passwords do not match'

# Test user registration with long first name
def test_signup_long_first_name(session):
    session.delete(f"{BASE_URL}/clear")
    invalid_data = valid_registration_data1.copy()
    invalid_data['firstName'] = 'a' * 16
    response = session.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'First name cannot exceed 15 characters'

# Test user registration with empty first name
def test_signup_first_name_empty(session):
    session.delete(f"{BASE_URL}/clear")
    invalid_data = valid_registration_data1.copy()
    invalid_data['firstName'] = ''
    response = session.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'First name cannot be empty'

# Test user registration with long last name
def test_signup_last_name_too_long(session):
    session.delete(f"{BASE_URL}/clear")
    invalid_data = valid_registration_data1.copy()
    invalid_data['lastName'] = 'a' * 16
    response = session.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Last name cannot exceed 15 characters'

# Test user registration with empty last name
def test_signup_last_name_empty(session):
    session.delete(f"{BASE_URL}/clear")
    invalid_data = valid_registration_data1.copy()
    invalid_data['lastName'] = ''
    response = session.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Last name cannot be empty'

# Test user registration with invalid email
def test_signup_invalid_email(session):
    session.delete(f"{BASE_URL}/clear")
    invalid_data = valid_registration_data1.copy()
    invalid_data['email'] = 'example.com'
    response = session.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Email must be of a valid format'

# Test user registration with short password
def test_signup_password_too_short(session):
    session.delete(f"{BASE_URL}/clear")
    invalid_data = valid_registration_data1.copy()
    invalid_data['password'] = 'a1'
    invalid_data['confirmPassword'] = 'a1'
    response = session.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Password should be atleast 8 characters'

# Test user registration with long password
def test_signup_password_too_long(session):
    session.delete(f"{BASE_URL}/clear")
    invalid_data = valid_registration_data1.copy()
    invalid_data['password'] = 'a1' * 8
    invalid_data['confirmPassword'] = 'a1' * 8
    response = session.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Password shouldn\'t exceed 15 characters'

# Test user registration with password not containing numbers
def test_signup_password_does_not_contain_number(session):
    session.delete(f"{BASE_URL}/clear")
    invalid_data = valid_registration_data1.copy()
    invalid_data['password'] = 'p' * 9
    invalid_data['confirmPassword'] = 'p' * 9
    response = session.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Password should contain atleast one letter and one number'

# Test user registration with password not containing letters
def test_signup_password_does_not_contain_letter(session):
    session.delete(f"{BASE_URL}/clear")
    invalid_data = valid_registration_data1.copy()
    invalid_data['password'] = '1' * 9
    invalid_data['confirmPassword'] = '1' * 9
    response = session.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Password should contain atleast one letter and one number'

# Test successful login
def test_login_successful(session):
    session.delete(f"{BASE_URL}/clear")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    response = session.post(f"{BASE_URL}/auth/login", data=valid_login_data)
    assert response.status_code == 200       # May need to test each function 

# Test login with incorrect password
def test_login_incorrect_password(session):
    session.delete(f"{BASE_URL}/clear")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    invalid_data = valid_login_data.copy()
    invalid_data['password'] = 'p0sswords'
    response = session.post(f"{BASE_URL}/auth/login", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Invalid email and/or password'

# Test login for user that doesn't exist
def test_login_user_does_not_exist(session):
    session.delete(f"{BASE_URL}/clear")
    response = session.post(f"{BASE_URL}/auth/login", data=valid_login_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Invalid email and/or password'

def test_logout_success(session):
    session.delete(f"{BASE_URL}/clear")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data)
    response1 = session.get(f"{BASE_URL}/auth/logout")
    assert response1.status_code == 200
    response2 = session.get(f"{BASE_URL}/mailbox")
    assert response2.status_code == 400
    message = response2.json()
    assert message['error'] == 'Invalid userId'

def test_logout_when_not_logged_in_success(session):
    session.delete(f"{BASE_URL}/clear")
    response = session.get(f"{BASE_URL}/auth/logout")
    assert response.status_code == 200




