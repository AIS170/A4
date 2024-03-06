import uuid
import re

# Registers a new user and redirects them to their mailbox
def signup(firstName: str, lastName: str, email: str, password: str, confirmPassword: str) -> str:
    if password != confirmPassword:
        raise ValueError("Password doesn't match")
    elif len(firstName) > 15:
        raise ValueError("First name cannot exceed 15 characters")
    elif len(firstName) == 0:
        raise ValueError("First name cannot be empty")
    elif len(lastName) > 15:
        raise ValueError("Last name cannot exceed 15 characters")
    elif len(lastName) == 0:
        raise ValueError("Last name cannot be empty")
    elif not validEmail(email):
        raise ValueError("Email must be of a valid format")
    elif len(password) < 8:
        raise ValueError("Password should be atleast 8 characters")
    elif len(password) > 15:
        raise ValueError("Password shouldn't exceed 15 characters")
    elif not (any(char.isalpha() for char in password) and any(char.isdigit() for char in password)):
        raise ValueError("Password should contain atleast one letter and one number")
    else:
        return uuid.uuid4()

def validEmail(email: str) -> bool:
    regexPattern = pattern = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'
    if re.match(regexPattern, email):
        return True
    else:
        return False

# Login page for registered users. Redirects the user to their mailbox
def login(email: str, password: str) -> str:
    return 'u1'