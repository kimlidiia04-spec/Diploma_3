import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class OrderFeedPage(BasePage):

    TOTAL_COMPLETED = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")
    TODAY_COMPLETED = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    
    IN_PROGRESS_ORDER = (By.XPATH, "//li[contains(@class, 'text_type_digits-default') and text()='{}']")
    
    def get_in_progress_order_locator(self, order_number):
        return (By.XPATH, self.IN_PROGRESS_ORDER[1].format(order_number))

    def wait_feed_loaded(self):
        self.wait.until(lambda d: d.find_element(*self.TOTAL_COMPLETED).text not in ("", "0"))

    @allure.step("Получить счётчик «Выполнено за всё время»")
    def get_total_completed(self):
        self.wait_feed_loaded()
        return int(self.get_text(self.TOTAL_COMPLETED))

    @allure.step("Получить счётчик «Выполнено за сегодня»")
    def get_today_completed(self):
        self.wait_feed_loaded()
        return int(self.get_text(self.TODAY_COMPLETED))

    @allure.step("Проверить, что счётчик «Выполнено за всё время» увеличился")
    def is_total_completed_increased(self, value_before):
        return self.long_wait.until(lambda d: int(d.find_element(*self.TOTAL_COMPLETED).text) > value_before)

    @allure.step("Проверить, что счётчик «Выполнено за сегодня» увеличился")
    def is_today_completed_increased(self, value_before):
        return self.long_wait.until(lambda d: int(d.find_element(*self.TODAY_COMPLETED).text) > value_before)

    @allure.step("Проверить, что заказ есть в разделе «В работе»")
    def is_order_in_progress(self, order_number):
        locator = self.get_in_progress_order_locator(order_number)
        return self.long_wait.until(EC.visibility_of_element_located(locator)).is_displayed()