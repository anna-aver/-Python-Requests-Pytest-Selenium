import pytest
import time

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from info.default_data import Dflt

def test_positive_login(browser):
    """
    TRP-1. Positive case
    """
    browser.get(url=f'{Dflt.URL}/login')

    # поиск и заполнение поля "Почта"
    email_input = browser.find_element(by=By.CSS_SELECTOR, value='[class*="k_form_f_email"]')
    email_input.click()
    email_input.send_keys(Dflt.VALID['email'])

    # поиск и заполнение поля "Пароль"
    password_input = browser.find_element(by=By.ID, value='k_password')
    password_input.click()
    password_input.send_keys(Dflt.VALID['password'])

    # поиск и нажатие кнопки "Войти"
    button = browser.find_element(by=By.CSS_SELECTOR, value='[class*="k_form_send_auth"]')
    button.click()

    # Ожидание загрузки страницы
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be(f'{Dflt.URL}/'))

    # Поиск элемента, где указан id тренера, и запись его значения в переменную
    trainer_id = browser.find_element(by=By.CSS_SELECTOR, value='[class="header_card_trainer_id_num"]').text
    
    # Сравнение найденного id тренера с ожидаемым
    assert trainer_id == Dflt.TRAINER_ID, 'Unexpected trainer id'

CASES = [
    ('1', Dflt.INVALID['email'], Dflt.VALID['password'], 'Введите корректную почту'),
    ('2', Dflt.VALID['email'], Dflt.INVALID['password'], 'Неверные логин или пароль'),
    ('3', Dflt.INVALID['email'], Dflt.INVALID['password'], 'Введите корректную почту'),
    ('4', '', Dflt.VALID['password'], 'Введите почту'),
    ('5', Dflt.VALID['email'], '', 'Введите пароль')
]

@pytest.mark.parametrize('case_number, email, password, alerts', CASES)
def test_negative_login(case_number, email, password, alerts, browser):
    """
    TRP-2. Negative cases
    """

    logger.info(f'CASE : {case_number}')
    browser.get(url=f'{Dflt.URL}/login')

    # поиск и заполнение поля "Почта"
    email_input = browser.find_element(by=By.CSS_SELECTOR, value='[class*="k_form_f_email"]')
    email_input.click()
    email_input.send_keys(email)

    # поиск и заполнение поля "Пароль"
    password_input = browser.find_element(by=By.ID, value='k_password')
    password_input.click()
    password_input.send_keys(password)

    # поиск и нажатие кнопки "Войти"
    button = browser.find_element(by=By.CSS_SELECTOR, value='[class*="k_form_send_auth"]')
    button.click()
    
    # ожидание 2сек.
    time.sleep(2)

    # поиск сообщений о ошибке и сохранение текста
    alerts_messages = browser.find_element(by=By.CSS_SELECTOR, value='[class*="auth__error"]')

    # сравнение текста об ошибке с ожидаемым
    assert alerts_messages.text == alerts, 'Unexpected alerts in authentification form'