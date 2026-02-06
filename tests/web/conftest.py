import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# фикстура для каждой функции теста
@pytest.fixture(scope='function')
def browser():
    """
    Basic fixture
    """
    # Опции для запуска браузера
    chrome_options = Options() # создание объекта для настройки браузера
    chrome_options.add_argument("--no-sandbox") # отключение использования изолированной среды
    chrome_options.add_argument("start-maximized") # открытие браузера на полный экран
    chrome_options.add_argument("--disable-infibars") # отключение инфо сообщений
    chrome_options.add_argument("--disable-extensions") # отключение расширений
    chrome_options.add_argument("--disable-gpu") # отключение GPU
    chrome_options.add_argument("--disable-dev-shm-usage") # отключение использования разделяемой памяти, использование всей памяти
    #chrome_options.add_argument("--headless") # спец. режим "без браузера"

    # установка webdriver в соответствии с версией используемого браузера
    service = Service()
    # запускаем браузер с указанными выше настройками
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # переход к выполнению тестов (разделитель: все, что написано над ним, будет исполнено до теста, все, что ниже - после теста)
    yield driver
    # закрытие браузера после теста
    driver.close
