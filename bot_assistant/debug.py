import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/102.0.5005.134 YaBrowser/22.7.0.1842 Yowser/2.5 Safari/537.36')


driver = webdriver.Chrome(executable_path='handlers/chromedriver.exe', chrome_options=chrome_options)

try:
    driver.get('https://ru.hitmotop.com/')
    time.sleep(2)
    city_input = driver.find_element(by=By.CLASS_NAME, value='form-control')
    city_input.clear()
    city_input.send_keys('Экспайн')
    time.sleep(2)
    city_input.send_keys(Keys.ENTER)
    time.sleep(2)
    name = driver.find_elements(by=By.CLASS_NAME, value='track__title')
    for el in name:
        print(el.text)

except Exception as err:
    print(err)
finally:
    driver.close()
    driver.quit()