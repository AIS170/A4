import json



JSON_FILE_PATH = 'users.json'
# Function to load data from JSON file
def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"users": []}
    return data

# Function to save data to JSON file
def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Function to add a new user
def add_user(user_id, first_name, last_name, email, password, file_path):
    data = load_data(file_path)
    user = {
        "user_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    }
    data["users"].append(user)
    save_data(data, file_path)

