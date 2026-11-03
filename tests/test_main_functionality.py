import allure

from data import FEED_URL, FILLING_NAME, STELLAR_BURGERS_URL
from pages.main_page import MainPage

@allure.epic("Конструктор бургеров")
@allure.feature("Проверка основной функциональности")
class TestMainFunctionality:

    @allure.title("01. Переход по клику на «Конструктор»")
    def test_click_constructor(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.click_order_feed()
        main_page.click_constructor()
        assert main_page.is_url_opened(STELLAR_BURGERS_URL), "Клик по «Конструктор» должен вести на главную страницу"

    @allure.title("02. Переход по клику на «Лента заказов»")
    def test_click_order_feed(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.click_order_feed()
        assert main_page.is_url_opened(FEED_URL), "Клик по «Лента заказов» должен вести на страницу ленты заказов"

    @allure.title("03. При клике на ингредиент появляется окно с деталями")
    def test_ingredient_modal_opens(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.click_ingredient(FILLING_NAME)
        assert main_page.is_ingredient_modal_displayed(), "Должно появиться окно «Детали ингредиента»"

    @allure.title("04. Окно с деталями ингредиента закрывается по клику на крестик")
    def test_ingredient_modal_closes(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.click_ingredient(FILLING_NAME)
        main_page.close_modal()
        assert main_page.is_ingredient_modal_closed(), "Окно «Детали ингредиента» должно закрыться"

    @allure.title("05. При добавлении ингредиента в заказ его счётчик увеличивается")
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.add_ingredient(FILLING_NAME)
        assert main_page.get_ingredient_counter(FILLING_NAME) == "1", "Счётчик ингредиента должен стать равным 1"