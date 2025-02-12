from .base_page import BasePage
from .locators import BasketPageLocators


class BasketPage(BasePage):

    def should_be_empty_basket(self):
        """ Проверка, что корзина пуста (нет товаров) """
        assert self.is_not_element_present(*BasketPageLocators.BASKET_ITEMS), "Basket is not empty"

    def should_be_empty_basket_message(self):
        """ Проверка, что отображается сообщение о пустой корзине """
        assert self.is_element_present(
            *BasketPageLocators.EMPTY_BASKET_MESSAGE), "Empty basket message is not displayed"

