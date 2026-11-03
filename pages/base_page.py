import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 10
LONG_TIMEOUT = 30

DRAG_AND_DROP_SCRIPT = """
const dataTransfer = new DataTransfer();
const fire = (element, type) => element.dispatchEvent(
    new DragEvent(type, {bubbles: true, cancelable: true, dataTransfer: dataTransfer})
);
fire(arguments[0], 'dragstart');
fire(arguments[1], 'dragenter');
fire(arguments[1], 'dragover');
fire(arguments[1], 'drop');
fire(arguments[0], 'dragend');
"""


class BasePage:

    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, "//a[@href='/feed']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
        self.long_wait = WebDriverWait(driver, LONG_TIMEOUT)

    @allure.step("Открыть страницу {url}")
    def open(self, url):
        self.driver.get(url)
        return self

    @allure.step("Дождаться элемента и кликнуть по нему")
    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step('Ввести текст "{text}" в поле')
    def type_text(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента")
    def get_text(self, locator):
        element = self.wait_visible(locator)
        return element.text

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Проверить отображение элемента")
    def is_displayed(self, locator):
        return self.wait_visible(locator).is_displayed()

    @allure.step("Дождаться, пока элемент исчезнет")
    def wait_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    @allure.step("Проверить, что открыт адрес {url}")
    def is_url_opened(self, url):
        return self.wait.until(EC.url_to_be(url))

    @allure.step("Перетащить элемент в заданную область")
    def drag_and_drop(self, source_locator, target_locator):
        source = self.wait_visible(source_locator)
        target = self.wait_visible(target_locator)
        self.driver.execute_script(DRAG_AND_DROP_SCRIPT, source, target)

    @allure.step("Нажать «Конструктор»")
    def click_constructor(self):
        self.click(self.CONSTRUCTOR_BUTTON)

    @allure.step("Нажать «Лента заказов»")
    def click_order_feed(self):
        self.click(self.ORDER_FEED_BUTTON)