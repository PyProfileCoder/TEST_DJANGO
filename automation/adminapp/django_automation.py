import requests
from requests.auth import HTTPBasicAuth

# Configuration
ADMIN_BASE_URL = 'http://127.0.0.1:8000/admin'  # Replace with your admin base URL
USERNAME = 'admin'  # Replace with your admin username
PASSWORD = 'admin'  # Replace with your admin password

# Admin API endpoints you want to check
ADMIN_API_ENDPOINTS = [
    '/auth/user/',           # Example: User list
    '/auth/group/',          # Example: Group list
    '/finance/expenses/',         # Replace with your app and model
    '/anotherapp/othermodel/' # Add more admin endpoints here
]

CSRF_TOKEN_KEY = 'csrftoken'

# Function to login to Django admin
def login_to_admin():
    login_url = f'{ADMIN_BASE_URL}/login/'
    session = requests.Session()

    # Fetch the login page first to get CSRF token
    response = session.get(login_url)
    csrftoken = response.cookies['csrftoken']

    # Prepare login data
    login_data = {
        'username': USERNAME,
        'password': PASSWORD,
        'csrfmiddlewaretoken': csrftoken,
        'next': '/admin/'
    }

    # Send login request with CSRF token
    headers = {
        'Referer': login_url
    }
    session.post(login_url, data=login_data, headers=headers)

    # Verify login was successful
    if session.cookies.get('sessionid'):
        print("Login successful!")
        return session
    else:
        print("Login failed!")
        return None

# Function to test an API endpoint
def check_admin_api(session, endpoint):
    url = f'{ADMIN_BASE_URL}{endpoint}'
    response = session.get(url)
    if response.status_code == 200:
        print(f"Success: {url} returned status code 200")
    else:
        print(f"Failed: {url} returned status code {response.status_code}")
    return response

# Function to add a group via POST request
def add_group(session, group_name):
    group_add_url = f'{ADMIN_BASE_URL}/auth/group/add/'  # Django admin endpoint to add groups
    csrftoken = session.cookies[CSRF_TOKEN_KEY]

    # POST data to create a new group
    group_data = {
        'name': group_name,
        'csrfmiddlewaretoken': csrftoken,
        '_save': 'Save'
    }

    headers = {
        'Referer': group_add_url
    }

    response = session.post(group_add_url, data=group_data, headers=headers)
    if response.status_code == 200 or response.status_code == 302:
        print(f"Group '{group_name}' added successfully.")
    else:
        print(f"Failed to add group '{group_name}'. Status code: {response.status_code}")

# Function to add a user via POST request
def add_user(session, username, password, email):
    user_add_url = f'{ADMIN_BASE_URL}/auth/user/add/'  # Django admin endpoint to add users
    csrftoken = session.cookies[CSRF_TOKEN_KEY]

    # POST data to create a new user
    user_data = {
        'username': username,
        'password1': password,
        'password2': password,
        'email': email,
        'csrfmiddlewaretoken': csrftoken,
        '_save': 'Save'
    }

    headers = {
        'Referer': user_add_url
    }

    response = session.post(user_add_url, data=user_data, headers=headers)
    if response.status_code == 200 or response.status_code == 302:
        print(f"User '{username}' added successfully.")
    else:
        print(f"Failed to add user '{username}'. Status code: {response.status_code}")

# Function to delete a group via DELETE request
def delete_group(session, group_id):
    group_delete_url = f'{ADMIN_BASE_URL}/auth/group/{group_id}/delete/'  # Admin delete URL for group
    csrftoken = session.cookies[CSRF_TOKEN_KEY]

    # Send POST request to delete a group (Django uses POST for delete operations)
    delete_data = {
        'csrfmiddlewaretoken': csrftoken,
        'post': 'yes'  # This is needed to confirm the deletion in Django admin
    }

    headers = {
        'Referer': group_delete_url
    }

    response = session.post(group_delete_url, data=delete_data, headers=headers)
    if response.status_code == 200 or response.status_code == 302:
        print(f"Group with ID '{group_id}' deleted successfully.")
    else:
        print(f"Failed to delete group with ID '{group_id}'. Status code: {response.status_code}")

# Function to delete a user via DELETE request
def delete_user(session, user_id):
    user_delete_url = f'{ADMIN_BASE_URL}/auth/user/{user_id}/delete/'  # Admin delete URL for user
    csrftoken = session.cookies[CSRF_TOKEN_KEY]

    # Send POST request to delete a user (Django uses POST for delete operations)
    delete_data = {
        'csrfmiddlewaretoken': csrftoken,
        'post': 'yes'  # This is needed to confirm the deletion in Django admin
    }

    headers = {
        'Referer': user_delete_url
    }

    response = session.post(user_delete_url, data=delete_data, headers=headers)
    if response.status_code == 200 or response.status_code == 302:
        print(f"User with ID '{user_id}' deleted successfully.")
    else:
        print(f"Failed to delete user with ID '{user_id}'. Status code: {response.status_code}")

def add_finance_expenses(session, expense_name):
    finance_add_url = f'{ADMIN_BASE_URL}/finance/expenses/add/'  # Django admin endpoint to add groups
    csrftoken = session.cookies[CSRF_TOKEN_KEY]
    from datetime import datetime
    current_date = datetime.now().strftime('%Y-%m-%d')

    # POST data to create a new group
    expenses_data = {
        'user': 2,
        'description': expense_name,
        'amount': 1000,
        'date':current_date,
        'csrfmiddlewaretoken': csrftoken,
        '_save': 'Save'
    }

    headers = {
        'Referer': finance_add_url
    }

    response = session.post(finance_add_url, data=expenses_data, headers=headers)
    if response.status_code == 200 or response.status_code == 302:
        print(f"Finance '{expense_name}' added successfully")
    else:
        print(f"Failed to add group '{expense_name}'. Status code: {response.status_code}")


# Main function to check all API endpoints
def check_all_admin_apis():
    session = login_to_admin()
    if session:
        for endpoint in ADMIN_API_ENDPOINTS:
            check_admin_api(session, endpoint)

         # Perform CRUD operations
        add_group(session, 'Test Group')
        add_user(session, 'testuser', 'password123', 'testuser@example.com')
        add_finance_expenses(session, 'ADD_EXPENSE')
        # Assume we want to delete the first group with ID 1 and user with ID 1 (replace with actual IDs)
        # delete_finance_expenses(session,)
        delete_group(session, 1)
        delete_user(session, 1)

    else:
        print("Skipping API checks due to failed login.")

if __name__ == '__main__':
    check_all_admin_apis()
