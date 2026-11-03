import allure
from selenium.webdriver.common.by import By

from data import STELLAR_BURGERS_URL, BUN_NAME, FILLING_NAME
from pages.base_page import BasePage


class MainPage(BasePage):

    INGREDIENT = (By.XPATH, "//p[text()='{}']/parent::a")
    INGREDIENT_COUNTER = (By.XPATH, "//p[text()='{}']/parent::a//p[contains(@class, 'counter_counter__num')]")

    CONSTRUCTOR_AREA = (By.XPATH, "//section[contains(@class, 'BurgerConstructor_basket')]")

    INGREDIENT_MODAL_TITLE = (By.XPATH, "//h2[text()='Детали ингредиента']")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")

    MAKE_ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")

    def get_ingredient_locator(self, name):
        return (By.XPATH, self.INGREDIENT[1].format(name))

    def get_ingredient_counter_locator(self, name):
        return (By.XPATH, self.INGREDIENT_COUNTER[1].format(name))

    @allure.step("Открыть главную страницу")
    def open_main_page(self):
        self.open(STELLAR_BURGERS_URL)

    @allure.step("Кликнуть по ингредиенту")
    def click_ingredient(self, name):
        self.click(self.get_ingredient_locator(name))

    @allure.step("Проверить, что окно с деталями ингредиента открыто")
    def is_ingredient_modal_displayed(self):
        return self.is_displayed(self.INGREDIENT_MODAL_TITLE)

    @allure.step("Закрыть всплывающее окно")
    def close_modal(self):
        self.click(self.MODAL_CLOSE_BUTTON)

    @allure.step("Проверить, что окно с деталями ингредиента закрыто")
    def is_ingredient_modal_closed(self):
        return self.wait_invisible(self.INGREDIENT_MODAL_TITLE)

    @allure.step("Добавить ингредиент в заказ")
    def add_ingredient(self, name):
        self.drag_and_drop(self.get_ingredient_locator(name), self.CONSTRUCTOR_AREA)

    @allure.step("Получить счётчик ингредиента")
    def get_ingredient_counter(self, name):
        return self.get_text(self.get_ingredient_counter_locator(name))

    @allure.step("Получить номер оформленного заказа")
    def get_order_number(self):
        self.long_wait.until(lambda d: d.find_element(*self.ORDER_NUMBER).text not in ("", "9999"))
        return self.get_text(self.ORDER_NUMBER)

    @allure.step("Оформить заказ")
    def make_order(self):
        self.add_ingredient(BUN_NAME)
        self.add_ingredient(FILLING_NAME)
        self.click(self.MAKE_ORDER_BUTTON)
        return self.get_order_number()

    @allure.step("Закрыть окно с номером заказа")
    def close_order_modal(self):
        self.click(self.MODAL_CLOSE_BUTTON)
        self.wait_invisible(self.ORDER_NUMBER)