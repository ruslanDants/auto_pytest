import math

from selenium.common import NoAlertPresentException

from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):

    def should_be_add_to_basket_button(self):
        assert self.is_element_present(*ProductPageLocators.ADD_TO_BASKET_BUTTON), "Add to basket button not presented"


    def should_be_name_of_product(self):
        assert self.is_element_present(*ProductPageLocators.NAME_OF_PRODUCT), "Name of product don't found"


    def get_product_name(self):
        self.should_be_name_of_product()
        return self.browser.find_element(*ProductPageLocators.NAME_OF_PRODUCT).text


    def should_be_price_of_product(self):
        assert self.is_element_present(*ProductPageLocators.PRODUCT_PRICE), "Product Price not found"


    def get_product_price(self):
        self.should_be_price_of_product()
        return self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text


    def should_be_product_info(self):
        self.should_be_name_of_product()
        self.should_be_price_of_product()
        self.should_be_add_to_basket_button()

    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Success message is presented, but should not be"

    def should_be_msg_about_adding_product(self, product_name):
        # Проверка выхода сообщения что товар добавлен
        product_from_message = self.browser.find_element(*ProductPageLocators.MESSAGE_ABOUT_ADDING).text
        print(product_from_message)
        assert product_from_message == product_name, "Wrong product in text message"


    def compare_basket_to_product_price(self, product_price):
        # Сравнение цен товара и пустой корзины
        basket_price = self.browser.find_element(*ProductPageLocators.BASKET_PRICE).text

        assert product_price == basket_price, "Product price and basket price is not equal"


    def solve_quiz_and_get_code(self):
        # Для решения задачки внутри алерта
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs((12 * math.sin(float(x))))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")


    def add_product_to_basket(self):
        add_to_basket_button = self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BUTTON)
        add_to_basket_button.click()

        # self.solve_quiz_and_get_code()