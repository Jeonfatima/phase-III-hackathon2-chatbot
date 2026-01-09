import os
import requests
import json

# Set environment variables
os.environ['BETTER_AUTH_SECRET'] = 'your-super-secret-key-for-dev-testing'
os.environ['DATABASE_URL'] = 'sqlite:///./todoapp.db'

def test_user_creation():
    url = "http://127.0.0.1:8000/api/auth/sign-up"

    # First, try to create a user
    user_data = {
        "email": "testfinal@example.com",
        "password": "testpassword123"
    }
    headers = {"Content-Type": "application/json"}

    print("Testing user creation...")
    response = requests.post(url, data=json.dumps(user_data), headers=headers)
    print(f"First request - Status Code: {response.status_code}")
    print(f"First request - Response: {response.text}")

    if response.status_code == 200:
        print("\nFirst user created successfully!")
        # Now try to create the same user again to test if it exists
        print("\nTrying to create the same user again (should fail)...")
        response2 = requests.post(url, data=json.dumps(user_data), headers=headers)
        print(f"Second request - Status Code: {response2.status_code}")
        print(f"Second request - Response: {response2.text}")
    else:
        print(f"\nFirst user creation failed with status: {response.status_code}")

if __name__ == "__main__":
    test_user_creation()