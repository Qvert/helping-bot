import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from loguru import logger

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/102.0.5005.134 YaBrowser/22.7.0.1842 Yowser/2.5 Safari/537.36')
chrome_options.headless = True
driver = webdriver.Chrome(executable_path='handlers/chromedriver.exe', chrome_options=chrome_options)

try:
    driver.get('https://www.timeserver.ru')
    city_input = driver.find_element(by=By.NAME, value='q')
    city_input.clear()
    city_input.send_keys('Москва')

    city_input.send_keys(Keys.ENTER)

    zone_time = driver.find_elements(by=By.TAG_NAME, value='span')
    zone_time = [el.text.strip() for el in zone_time][18]
    print(zone_time)

except Exception as err:
    logger.error(err)
finally:
    driver.close()
    driver.quit()
