import pytest
from auth import signup

@pytest.fixture
def test_signup_successful():
    user_id = signup('first', 'user', 'user@example.com', 'validPassword100', 'validPassword100')
    print(user_id)
    assert isinstance(user_id, str)

def signup_test_email_in_use():
    signup('first', 'user', 'user@example.com', 'validPassword100', 'validPassword100')
    with pytest.raises(ValueError) as exc_info:
        signup('second', 'user', 'user@example.com', 'validPassword101', 'validPassword101')
    
    assert str(exc_info.value) == "Email is already in use"

def signup_test_password_not_matching():
    with pytest.raises(ValueError) as exc_info:
        signup('second', 'user', 'user@example.com', 'validPassword100', 'validPassword101')
    
    assert str(exc_info.value) == "Password doesn't match"

def signup_test_first_name_too_long():
    with pytest.raises(ValueError) as exc_info:
        signup('secondsecondsecond', 'user', 'user@example.com', 'validPassword100', 'validPassword101')
    
    assert str(exc_info.value) == "First name cannot exceed 15 characters"