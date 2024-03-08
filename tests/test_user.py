import pytest
import requests
from user import userDetails, updateEmail, updatePassword, userLogout

BASE_URL = "http://localhost:5000"

# # Dummy data for testing purposes
# valid_user_id = "valid_user_id"
# invalid_user_id = "invalid_user_id"
# new_email = "newemail@example.com"
# new_password = "NewP@ssw0rd!"

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

# User Details Tests:
# Success test for getting correct user details in dict form.
def test_get_user_details_success():
    response = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    valid_user_id = response.json()['userId']
    response1 = requests.get(f"{BASE_URL}/user/details", params={"userId": valid_user_id})
    assert response1.status_code == 200
    assert isinstance(response1.json(), dict)


# Fail to get user details, due to invalid user_id.
def test_get_user_details_failure():
    response = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    valid_user_id = response.json()['userId']
    response1 = requests.get(f"{BASE_URL}/user/details", params={"userId": valid_user_id + 'a'})
    assert response1.status_code == 400


# Change Email Tests:
# Success test for changing email
def test_change_email_success():
    response1 = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    valid_user_id = response1.json()['userId']
    response = requests.put(f"{BASE_URL}/user/email", json={'user_id': valid_user_id, 'email': "user222@example.com"})
    assert response.status_code == 200
    response3 = requests.get(f"{BASE_URL}/user/details", params={"userId": valid_user_id})
    assert response3.json().get("email") == "user222@example.com"


# Fail to change email
def test_change_email_failure_invalid_user():
    response1 = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    valid_user_id = response1.json()['userId']
    response = requests.put(f"{BASE_URL}/user/email", json={'user_id': valid_user_id + 'a', 'email': "user222@example.com"})
    assert response.status_code == 400


# Change Password Tests:
# Success test for changing password
def test_change_password_success():
    response1 = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    valid_user_id = response1.json()['userId']
    response = requests.put(f"{BASE_URL}/user/password", json={'user_id': valid_user_id, 'password': "val1dPassword222"})
    assert response.status_code == 200
    response3 = requests.get(f"{BASE_URL}/user/details", params={"userId": valid_user_id})
    assert response3.json().get("password") == "val1dPassword222"


# Fail to change password
def test_change_password_failure_invalid_user():
    response1 = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    valid_user_id = response1.json()['userId']
    response = requests.put(f"{BASE_URL}/user/password", json={'user_id': valid_user_id + 'a', 'email': "val1dPassword222"})
    assert response.status_code == 400


# Logout Tests:
# Success test for logging user out
def test_logout_success():
    response1 = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    valid_user_id = response1.json()['userId']
    response = requests.post(f"{BASE_URL}/user/logout", data={"userId": valid_user_id})
    assert response.status_code == 200  # Could also add in 204 code


# Fail to log user out
def test_logout_failure():
    response1 = requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    valid_user_id = response1.json()['userId']
    response = requests.post(f"{BASE_URL}/user/logout", data={"userId": valid_user_id + 'a'})
    assert response.status_code == 400
