import random
import string

import allure
import requests

from data import STELLAR_BURGERS_URL

def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

@allure.step("Подготовить данные для создания пользователя")
def get_user_payload():
    return {
        "email": f"{generate_random_string()}@example.com",
        "password": generate_random_string(),
        "name": "Test",
    }

@allure.step("Отправить запрос на создание пользователя")
def create_user(payload):
    return requests.post(f"{STELLAR_BURGERS_URL}api/auth/register", json=payload)

@allure.step("Отправить запрос на авторизацию пользователя")
def login_user(payload):
    return requests.post(f"{STELLAR_BURGERS_URL}api/auth/login", json=payload)