import auth.py

# Stub code for authorisation functions

# Returns user details based on userId input, includes name, email, password, dateRegistered.
def userDetails(userId: str) -> list:

    return userDetails


# Updates and returns email for given user through userId and old email. Returns error message if update fails.
def updateEmail(email: str, userId: str) -> str:

    return email

# Updates and returns password for given user through userId and old password. Returns error message if update fails.
def updatePassword(userId: str, password: str, confirmPassword: str) -> str:

    return password

# Logs registered user out and redirects them to login/signup page.
def userLogout(userId: str) -> None:

    return None