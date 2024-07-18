import warnings
from schemas import User
import requests
import random
import string

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_email(domain='example.com', length=10):
    username = generate_random_string(length)
    return f"{username}@{domain}"

def generate_password(length=12):
    return generate_random_string(length)

def generate_full_name():
    first_name = generate_random_string(random.randint(3, 10))
    last_name = generate_random_string(random.randint(3, 10))
    return f"{first_name} {last_name}"

def generate_salary():
    return round(random.uniform(20000, 150000), 2)

def generate_payment_info():
    return ''.join(random.choices(string.digits, k=16))

def generate_hashed_password(password):
    return generate_random_string(64)

def generate_salt():
    return generate_random_string(16)

def populate_users(n=1000):
    url = "https://127.0.0.1:8000/users/add"
    headers = {"Content-Type": "application/json"}

    for _ in range(n):
        password = generate_password()
        U = User(
            email=generate_email(),
            password=password,
            full_name=generate_full_name(),
            salary=generate_salary(),
            payment_info=generate_payment_info(),
            hashed_pw=generate_hashed_password(password),
            salt=generate_salt()
        )
        user_dict = U.dict()

        response = requests.post(url, json=user_dict, headers=headers, verify=False)
        
        print(response)
        if response.status_code != 200:
            print(f"Error creating user: {response.text}")
        else:
            print(f"User created: {U.email}")

if __name__ == "__main__":
    populate_users()
