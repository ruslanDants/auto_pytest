import time

import pytest
from .pages.basket_page import BasketPage
from .pages.locators import ProductPageLocators
from .pages.login_page import LoginPage
from .pages.product_page import ProductPage

# Базовая ссылка на страницу товара
PRODUCT_PAGE_LINK = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"


@pytest.mark.login_user
class TestUserAddToBasketFromProductPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        """
        Фикстура для регистрации нового пользователя перед тестами.
        """
        login_link = "http://selenium1py.pythonanywhere.com/accounts/login/"
        page = LoginPage(browser, login_link)
        page.open()
        email = str(time.time()) + "@fakemail.org"
        password = "TestPassword123!"
        page.register_new_user(email, password)
        page.should_be_authorized_user()


    @pytest.mark.need_review
    def test_user_can_add_product_to_basket(self, browser):
        """
        Проверяет, что зарегистрированный пользователь может добавить товар в корзину.
        """
        product_page = ProductPage(browser, PRODUCT_PAGE_LINK)
        product_page.open()
        product_page.should_be_product_info()

        product_name = product_page.get_product_name()
        product_price = product_page.get_product_price()

        product_page.add_product_to_basket()

        product_page.should_be_msg_about_adding_product(product_name)
        product_page.compare_basket_to_product_price(product_price)


    def test_user_cant_see_success_message(self, browser):
        """
        Проверяет, что зарегистрированный пользователь не видит сообщения об успешном добавлении товара в корзину.
        """
        product_page = ProductPage(browser, PRODUCT_PAGE_LINK)
        product_page.open()
        product_page.should_not_be_success_message()


@pytest.mark.parametrize(
    'link',
    [
        f"{PRODUCT_PAGE_LINK}?promo=offer{i}" if i != 7
        else pytest.param(f"{PRODUCT_PAGE_LINK}?promo=offer7", marks=pytest.mark.xfail)
        for i in range(10)
    ]
)
@pytest.mark.need_review
def test_guest_can_add_product_to_basket(browser, link):
    """
    Проверяет, что гость может добавить товар в корзину.
    Тест с offer7 ожидаемо падает (xfail).
    """
    product_page = ProductPage(browser, link)
    product_page.open()
    product_page.should_be_product_info()

    product_name = product_page.get_product_name()
    product_price = product_page.get_product_price()

    # Добавить в корзину
    product_page.add_product_to_basket()
    product_page.solve_quiz_and_get_code()

    # Проверки
    product_page.should_be_msg_about_adding_product(product_name)
    product_page.compare_basket_to_product_price(product_price)


@pytest.mark.skip
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    """
    Проверяет, что после добавления товара в корзину сообщение об успешном добавлении не отображается.
    """
    product_page = ProductPage(browser, PRODUCT_PAGE_LINK)
    product_page.open()
    product_page.add_product_to_basket()
    assert product_page.is_not_element_present(
        *ProductPageLocators.SUCCESS_MESSAGE
    ), "Success message is displayed, but should not be"


@pytest.mark.skip
def test_guest_cant_see_success_message(browser):
    """
    Проверяет, что гость не видит сообщение об успешном добавлении товара до того, как он что-либо добавил в корзину.
    """
    product_page = ProductPage(browser, PRODUCT_PAGE_LINK)
    product_page.open()
    assert product_page.is_not_element_present(
        *ProductPageLocators.SUCCESS_MESSAGE
    ), "Success message is displayed, but should not be"


@pytest.mark.skip
def test_message_disappeared_after_adding_product_to_basket(browser):
    """
    Проверяет, что сообщение об успешном добавлении товара исчезает спустя некоторое время после добавления товара в корзину.
    """
    product_page = ProductPage(browser, PRODUCT_PAGE_LINK)
    product_page.open()
    product_page.add_product_to_basket()
    assert product_page.is_disappeared(
        *ProductPageLocators.SUCCESS_MESSAGE
    ), "Success message is still displayed, but should have disappeared"


def test_guest_should_see_login_link_on_product_page(browser):
    """
    Проверяет, что на странице товара присутствует ссылка для входа в систему.
    """
    page = ProductPage(browser, PRODUCT_PAGE_LINK)
    page.open()
    page.should_be_login_link()


@pytest.mark.need_review
def test_guest_can_go_to_login_page_from_product_page(browser):
    """
    Проверяет, что гость может перейти на страницу входа с страницы товара.
    """
    page = ProductPage(browser, PRODUCT_PAGE_LINK)
    page.open()
    page.go_to_login_page()


@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    """
    Гость открывает страницу товара, переходит в корзину и проверяет, что она пуста.
    """
    product_page = ProductPage(browser, PRODUCT_PAGE_LINK)
    product_page.open()
    product_page.go_to_basket()

    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_empty_basket()
    basket_page.should_be_empty_basket_message()
