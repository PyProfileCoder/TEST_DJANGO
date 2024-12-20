import requests

# Configure the API URLs
BASE_URL = 'http://127.0.0.1:8000/admin/'  # Admin base URL
LOGIN_URL = BASE_URL + 'login/'  # Admin login URL
ADD_QUESTION_URL = BASE_URL + 'polls/question/add/'
ADD_CHOICE_URL = BASE_URL + 'polls/choice/add/'
DELETE_QUESTION_URL = BASE_URL + 'polls/question/'
DELETE_CHOICE_URL = BASE_URL + 'polls/choice/'

# Configuration
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
    login_url = f'{BASE_URL}/login/'
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
        print(f"Failed to log in: {response.status_code}")
        print(response.text)  # Print the response for debugging
        return None


# Function to add a question via the admin API
def add_question(session, question_text, pub_date):
    # Get CSRF token from session for the post request
    csrf_token = session.cookies.get('csrftoken')

    payload = {
        'question_text': question_text,
        'pub_date': pub_date,
        'csrfmiddlewaretoken': csrf_token,
    }

    response = session.post(ADD_QUESTION_URL, data=payload, headers={'Referer': ADD_QUESTION_URL})

    if response.status_code == 201:
        question_id = response.json().get('id')
        print(f"Question added successfully: {question_text} (ID: {question_id})")
        return question_id
    else:
        print(f"Failed to add question: {response.status_code}")
        return None

# Function to add a choice to a question via the admin API
def add_choice(session, question_id, choice_text):
    # Get CSRF token from session for the post request
    csrf_token = session.cookies.get('csrftoken')

    payload = {
        'question': question_id,
        'choice_text': choice_text,
        'votes': 0,
        'csrfmiddlewaretoken': csrf_token,
    }

    response = session.post(ADD_CHOICE_URL, data=payload, headers={'Referer': ADD_CHOICE_URL})

    if response.status_code == 201:
        choice_id = response.json().get('id')
        print(f"Choice added successfully: {choice_text} (ID: {choice_id})")
        return choice_id
    else:
        print(f"Failed to add choice: {response.status_code}")
        return None

# Function to delete a question via the admin API
def delete_question(session, question_id):
    url = DELETE_QUESTION_URL + str(question_id) + '/delete/'
    csrf_token = session.cookies.get('csrftoken')

    response = session.post(url, data={'csrfmiddlewaretoken': csrf_token}, headers={'Referer': url})

    if response.status_code == 204:
        print(f"Question ID {question_id} deleted successfully.")
    else:
        print(f"Failed to delete question: {response.status_code}")

# Function to delete a choice via the admin API
def delete_choice(session, choice_id):
    url = DELETE_CHOICE_URL + str(choice_id) + '/delete/'
    csrf_token = session.cookies.get('csrftoken')

    response = session.post(url, data={'csrfmiddlewaretoken': csrf_token}, headers={'Referer': url})

    if response.status_code == 204:
        print(f"Choice ID {choice_id} deleted successfully.")
    else:
        print(f"Failed to delete choice: {response.status_code}")

# Simulating exceptions for edge cases

# 1. Attempt to add a question with invalid data (missing fields)
def add_invalid_question(session):
    csrf_token = session.cookies.get('csrftoken')
    payload = {
        'pub_date': '2024-12-19',  # Missing 'question_text'
        'csrfmiddlewaretoken': csrf_token
    }
    response = session.post(ADD_QUESTION_URL, data=payload, headers={'Referer': ADD_QUESTION_URL})
    if response.status_code == 400:
        print(f"Validation error: {response.json()}")
    else:
        print(f"Unexpected response: {response.status_code}")

# 2. Try to delete a non-existent question
def delete_non_existent_question(session):
    non_existent_id = 99999  # Assume this ID does not exist
    delete_question(session, non_existent_id)

# Main function to automate the process
def main():
    # Login to Django admin
    session = login_to_admin()

    if session:

        # Add a valid question
        question_id = add_question(session, "What's your favorite programming language?", "2024-12-19")

        # Add choices to the question if the question was successfully added
        if question_id:
            add_choice(session, question_id, "Python")
            add_choice(session, question_id, "JavaScript")
            add_choice(session, question_id, "C++")

        # Try some error cases
        add_invalid_question(session)  # Validation error for missing 'question_text'
        delete_non_existent_question(session)  # Trying to delete a question that doesn't exist

        # Clean up: delete the question and associated choices if added successfully
        if question_id:
            delete_question(session, question_id)
        
        session.close()

if __name__ == "__main__":
    main()
