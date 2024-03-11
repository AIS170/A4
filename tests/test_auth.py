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

@pytest.fixture(autouse=True)
def setup():
    requests.delete(f"{BASE_URL}/clear")

#Test successful user registration
def test_signup_success():
    response = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    assert response.status_code == 200

# Test two successful user registrations
def test_signup_success_two_users():
    response1 = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    assert response1.status_code == 200
    response2 = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
    assert response2.status_code == 200

# # Test user registration with same email
# def test_signup_email_in_use():
#     response1 = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
#     assert response1.status_code == 200
#     assert 'userId' in response1.json()
#     response2 = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
#     assert response2.status_code == 400

# Test user registration with non matching passwords
def test_signup_password_not_matching():
    invalid_data = valid_registration_data1.copy()
    invalid_data['confirmPassword'] = 'val0dPassword'
    response = requests.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Passwords do not match'

# Test user registration with long first name
def test_signup_long_first_name():
    invalid_data = valid_registration_data1.copy()
    invalid_data['firstName'] = 'a' * 16
    response = requests.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'First name cannot exceed 15 characters'

# Test user registration with empty first name
def test_signup_first_name_empty():
    invalid_data = valid_registration_data1.copy()
    invalid_data['firstName'] = ''
    response = requests.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'First name cannot be empty'

# Test user registration with long last name
def test_signup_last_name_too_long():
    invalid_data = valid_registration_data1.copy()
    invalid_data['lastName'] = 'a' * 16
    response = requests.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Last name cannot exceed 15 characters'

# Test user registration with empty last name
def test_signup_last_name_empty():
    invalid_data = valid_registration_data1.copy()
    invalid_data['lastName'] = ''
    response = requests.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Last name cannot be empty'

# Test user registration with invalid email
def test_signup_invalid_email():
    invalid_data = valid_registration_data1.copy()
    invalid_data['email'] = 'example.com'
    response = requests.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Email must be of a valid format'

# Test user registration with short password
def test_signup_password_too_short():
    invalid_data = valid_registration_data1.copy()
    invalid_data['password'] = 'a1'
    invalid_data['confirmPassword'] = 'a1'
    response = requests.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Password should be atleast 8 characters'

# Test user registration with long password
def test_signup_password_too_long():
    invalid_data = valid_registration_data1.copy()
    invalid_data['password'] = 'a1' * 8
    invalid_data['confirmPassword'] = 'a1' * 8
    response = requests.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Password shouldn\'t exceed 15 characters'

# Test user registration with password not containing numbers
def test_signup_password_does_not_contain_number():
    invalid_data = valid_registration_data1.copy()
    invalid_data['password'] = 'p' * 9
    invalid_data['confirmPassword'] = 'p' * 9
    response = requests.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Password should contain atleast one letter and one number'

# Test user registration with password not containing letters
def test_signup_password_does_not_contain_letter():
    invalid_data = valid_registration_data1.copy()
    invalid_data['password'] = '1' * 9
    invalid_data['confirmPassword'] = '1' * 9
    response = requests.post(f"{BASE_URL}/auth/signup", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Password should contain atleast one letter and one number'

# Test successful login
def test_login_successful():
    requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    response = requests.post(f"{BASE_URL}/auth/login", data=valid_login_data)
    assert response.status_code == 200       # May need to test each function 

# Test login with incorrect password
def test_login_incorrect_password():
    requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    invalid_data = valid_login_data.copy()
    invalid_data['password'] = 'p0sswords'
    response = requests.post(f"{BASE_URL}/auth/login", data=invalid_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Invalid email and/or password'

# Test login for user that doesn't exist
def test_login_user_does_not_exist():
    response = requests.post(f"{BASE_URL}/auth/login", data=valid_login_data)
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Invalid email and/or password'

def test_logout_success():
    requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    requests.post(f"{BASE_URL}/auth/login", data=valid_login_data)
    requests.post(f"{BASE_URL}/auth/logout")
    response = requests.get(f"{BASE_URL}/mailbox")
    assert response.status_code == 400, 200
    message = response.json()
    assert message['error'] == 'Invalid userId'

# def test_logout_not_logged_in():
#     requests.post(f"{BASE_URL}/auth/logout")
#     response = requests.get(f"{BASE_URL}/mailbox")
#     assert response.status_code == 400
#     message = response.json()
#     assert message['error'] == 'error: Invalid userId'




