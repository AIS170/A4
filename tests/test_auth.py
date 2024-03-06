import pytest
import uuid
from auth import signup, login
from user import userLogout

def test_signup_successful():
    user_id = signup('first', 'user', 'user@example.com', 'val1dPassword', 'val1dPassword')
    assert isinstance(user_id, uuid.UUID)

def test_signup_successful_two_users():
    user_id_1 = signup('first', 'user', 'user@example.com', 'val1dPassword', 'val1dPassword')
    user_id_2 = signup('second', 'user', 'user2@example.com', 'val1dPassword', 'val1dPassword')
    assert isinstance(user_id_1, uuid.UUID)
    assert isinstance(user_id_2, uuid.UUID)
    assert user_id_1 != user_id_2                         # May not work (Maybe use assert equals)

def test_signup_email_in_use():
    signup('first', 'user', 'user@example.com', 'val1dPassword', 'val1dPassword')
    with pytest.raises(ValueError) as exc_info:
        signup('second', 'user', 'user@example.com', 'val1dPassword', 'val1dPassword')
    
    assert str(exc_info.value) == "Email is already in use"

def test_signup_password_not_matching():
    with pytest.raises(ValueError) as exc_info:
        signup('second', 'user', 'user@example.com', 'validPassword1', 'validPassword0')
    
    assert str(exc_info.value) == "Password doesn't match"

def test_signup_first_name_too_long():
    with pytest.raises(ValueError) as exc_info:
        signup('secondsecondsecond', 'user', 'user@example.com', 'val1dPassword', 'val1dPassword')
    
    assert str(exc_info.value) == "First name cannot exceed 15 characters"

def test_signup_first_name_empty():
    with pytest.raises(ValueError) as exc_info:
        signup('', 'user', 'user@example.com', 'val1dPassword', 'val1dPassword')
    
    assert str(exc_info.value) == "First name cannot be empty"

def test_signup_last_name_too_long():
    with pytest.raises(ValueError) as exc_info:
        signup('user', 'secondsecondsecond', 'user@example.com', 'val1dPassword', 'val1dPassword')
    
    assert str(exc_info.value) == "Last name cannot exceed 15 characters"

def test_signup_last_name_empty():
    with pytest.raises(ValueError) as exc_info:
        signup('First', '', 'user@example.com', 'val1dPassword', 'val1dPassword')
    
    assert str(exc_info.value) == "Last name cannot be empty"

def test_signup_invalid_email():
    with pytest.raises(ValueError) as exc_info:
        signup('First', 'user', 'userexamplecom', 'val1dPassword', 'val1dPassword')
    
    assert str(exc_info.value) == "Email must be of a valid format"

def test_signup_password_too_short():
    with pytest.raises(ValueError) as exc_info:
        signup('First', 'user', 'user@example.com', 'val1d', 'val1d')
    
    assert str(exc_info.value) == "Password should be atleast 8 characters"

def test_signup_password_too_long():
    with pytest.raises(ValueError) as exc_info:
        signup('First', 'user', 'user@example.com', 'val1dval1dval1dval1d', 'val1dval1dval1dval1d')
    
    assert str(exc_info.value) == "Password shouldn't exceed 15 characters"

def test_signup_password_does_not_contain_number():
    with pytest.raises(ValueError) as exc_info:
        signup('First', 'user', 'user@example.com', 'validPassword', 'validPassword')
    
    assert str(exc_info.value) == "Password should contain atleast one letter and one number"

def test_signup_password_does_not_contain_letter():
    with pytest.raises(ValueError) as exc_info:
        signup('First', 'user', 'user@example.com', '123456789', '123456789')
    
    assert str(exc_info.value) == "Password should contain atleast one letter and one number"

def test_login_successful():
    user_id_1 = signup('first', 'user', 'user@example.com', 'val1dPassword', 'val1dPassword')
    userLogout(user_id_1)
    user_id_2 = login('user@example.com', 'val1dPassword')
    assert isinstance(user_id_2, str)
    assert user_id_1 == user_id_2                         # May not work (Maybe use assert equals)

def test_login_incorrect_password():
    user_id_1 = signup('first', 'user', 'user@example.com', 'val1dPassword', 'val1dPassword')
    userLogout(user_id_1)
    with pytest.raises(ValueError) as exc_info:
        login('user@example.com', 'val0dPassword')
    
    assert str(exc_info.value) == "Password is incorrect"

def test_login_user_does_not_exist():
    with pytest.raises(ValueError) as exc_info:
        login('user@example.com', 'val1dPassword')
    
    assert str(exc_info.value) == "User email is not registered"


