from .pages.basket_page import BasketPage
from .pages.main_page import MainPage
from .pages.login_page import LoginPage

main_page_link = "http://selenium1py.pythonanywhere.com"

def test_guest_can_go_to_login_page(browser):
    """ Гость открывает главную страницу и может перейти на страницу авторизации """
    page = MainPage(browser, main_page_link)
    page.open()
    page.go_to_login_page()
    login_page = LoginPage(browser, browser.current_url)
    login_page.should_be_login_page()

def test_guest_should_see_login_link(browser):
    """ Гость открывает главную страницу и видит ссылку на страницу авторизации """
    page = MainPage(browser, main_page_link)
    page.open()
    page.should_be_login_link()

def test_guest_cant_see_product_in_basket_opened_from_main_page(browser):
    """ Гость открывает главную страницу, переходит в корзину и проверяет, что она пуста """
    main_page = MainPage(browser, main_page_link)
    main_page.open()
    main_page.go_to_basket()

    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_empty_basket()
    basket_page.should_be_empty_basket_message()