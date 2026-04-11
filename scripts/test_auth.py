import requests

BASE_URL = "http://localhost:8000"

def register_user():
    print("Registering user...")
    url = f"{BASE_URL}/register"
    data = {
        "username": "aura_test",
        "full_name": "Aura Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def login_user():
    print("\nLogging in...")
    url = f"{BASE_URL}/token"
    data = {
        "username": "aura_test",
        "password": "testpassword123"
    }
    response = requests.post(url, data=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"Token: {token}")
        return token
    else:
        print(f"Error: {response.json()}")
        return None

def test_chat(token):
    print("\nTesting chat with token...")
    url = f"{BASE_URL}/chat"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": "Hello Aura!", "mode": "default"}
    response = requests.post(url, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    register_user() # Create the test user
    token = login_user()
    if token:
        test_chat(token)
