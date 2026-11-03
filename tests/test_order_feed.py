import allure

from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

@allure.epic("Лента заказов")
@allure.feature("Проверка счётчиков и раздела «В работе»")
class TestOrderFeed:

    @allure.title("01. При создании заказа счётчик «Выполнено за всё время» увеличивается")
    def test_total_completed_increases(self, logged_in_driver):
        main_page = MainPage(logged_in_driver)
        order_feed_page = OrderFeedPage(logged_in_driver)
        main_page.click_order_feed()
        total_before = order_feed_page.get_total_completed()
        main_page.click_constructor()
        main_page.make_order()
        main_page.close_order_modal()
        main_page.click_order_feed()
        assert order_feed_page.is_total_completed_increased(total_before), "Счётчик «Выполнено за всё время» должен увеличиться"

    @allure.title("02. При создании заказа счётчик «Выполнено за сегодня» увеличивается")
    def test_today_completed_increases(self, logged_in_driver):
        main_page = MainPage(logged_in_driver)
        order_feed_page = OrderFeedPage(logged_in_driver)
        main_page.click_order_feed()
        today_before = order_feed_page.get_today_completed()
        main_page.click_constructor()
        main_page.make_order()
        main_page.close_order_modal()
        main_page.click_order_feed()
        assert order_feed_page.is_today_completed_increased(today_before), "Счётчик «Выполнено за сегодня» должен увеличиться"

    @allure.title("03. После оформления заказа его номер появляется в разделе «В работе»")
    def test_order_appears_in_progress(self, logged_in_driver):
        main_page = MainPage(logged_in_driver)
        order_feed_page = OrderFeedPage(logged_in_driver)
        order_number = main_page.make_order()
        main_page.close_order_modal()
        main_page.click_order_feed()
        assert order_feed_page.is_order_in_progress(order_number), "Номер заказа должен появиться в разделе «В работе»"