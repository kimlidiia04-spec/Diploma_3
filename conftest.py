import pytest
import requests
import os
from selenium import webdriver

from data import STELLAR_BURGERS_URL
from helpers import create_user, get_user_payload, login_user
from pages.login_page import LoginPage


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        if os.getenv("CI"):
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        browser = webdriver.Chrome(options=options)

    else:
        options = webdriver.FirefoxOptions()
        if os.getenv("CI"):
            options.add_argument("-headless")
        browser = webdriver.Firefox(options=options)

    if not os.getenv("CI"):
        browser.maximize_window()

    yield browser
    browser.quit()



@pytest.fixture
def delete_user():
    user_data = {}

    def set_user_data(email, password):
        user_data["email"] = email
        user_data["password"] = password

    yield set_user_data

    response = login_user(user_data)
    token = response.json()["accessToken"]
    requests.delete(f"{STELLAR_BURGERS_URL}api/auth/user", headers={"Authorization": token})


@pytest.fixture
def registered_user(delete_user):
    payload = get_user_payload()
    create_user(payload)
    delete_user(payload["email"], payload["password"])
    return payload

@pytest.fixture
def logged_in_driver(driver, registered_user):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.login(registered_user["email"], registered_user["password"])
    return driver