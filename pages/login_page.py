import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from data import LOGIN_URL, STELLAR_BURGERS_URL
from pages.base_page import BasePage


class LoginPage(BasePage):

    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")

    @allure.step("Открыть страницу входа")
    def open_login_page(self):
        self.open(LOGIN_URL)

    @allure.step("Войти в аккаунт")
    def login(self, email, password):
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.wait.until(EC.url_to_be(STELLAR_BURGERS_URL))