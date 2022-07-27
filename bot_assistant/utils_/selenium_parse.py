import os

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from loguru import logger

from bot_assistant.utils_.class_error import UncorrectedInputCity


def get_time_zone(query: str) -> None | str:
    """
    :param query: Get you tim_zone.
    :return: List or stroka time_zone.
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/102.0.5005.134 YaBrowser/22.7.0.1842 Yowser/2.5 Safari/537.36')

    chrome_options.headless = True

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    try:
        driver.get('https://www.timeserver.ru')
        logger.debug('Open source time_zone')
        city_input = driver.find_element(by=By.NAME, value='q')
        city_input.clear()
        city_input.send_keys(text_city := query)

        logger.info(f'Send search {text_city}')

        city_input.send_keys(Keys.ENTER)

        zone_time = driver.find_elements(by=By.TAG_NAME, value='span')
        zone_time = [el.text.strip() for el in zone_time][18]
        return zone_time

    except UncorrectedInputCity as err:
        logger.error(err)
        return
    finally:
        driver.close()
        driver.quit()