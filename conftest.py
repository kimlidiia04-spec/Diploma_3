import pytest
import requests
from selenium import webdriver

from data import STELLAR_BURGERS_URL
from helpers import create_user, get_user_payload, login_user
from pages.login_page import LoginPage


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browsers = {"chrome": webdriver.Chrome, "firefox": webdriver.Firefox}
    driver = browsers[request.param]()
    driver.maximize_window()

    yield driver

    driver.quit()


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