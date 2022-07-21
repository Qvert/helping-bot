import datetime
import os
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loguru import logger

from bot_assistant.keyboard import keyboard_plan
from bot_assistant.state_class.class_state import Scheduler_plan
from bot_assistant.utils_.class_error import UncorrectedInputCity
from bot_assistant.database.method_database import UsersData

db = UsersData()


async def welcome_message(message: Message):
    await message.answer(f'Вас приветствует планировщик\n'
                         f'Перед тем как использовать мой функционал\n'
                         f'Нужно провести настройку часового пояса')

    await message.answer(f'🛠 Выберите подходящую настройку.\n'
                         f'Часовой пояс по умолчанию: +00:00', reply_markup=keyboard_plan)


async def get_button_text_city(message: Message):
    await message.answer('Введите город в котором проживаете или находитесь рядом с ним')
    await Scheduler_plan.get_name_city.set()


async def city_input_user(message: Message, state: FSMContext):
    await message.answer('Сейчас мы установим ваш часовой пояс, пожалуйста ждите.')
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
        city_input.send_keys(text_city := message.text)

        logger.info(f'Send serach {text_city}')

        city_input.send_keys(Keys.ENTER)

        zone_time = driver.find_elements(by=By.TAG_NAME, value='span')
        zone_time = [el.text.strip() for el in zone_time][18]

        db.update_data_base(data='time_zone', value=zone_time, id_us=message.from_user.id)
        logger.debug('Update zone_tim succsefull')
        await message.answer(f'Ваш часовой пояс установлен на: {zone_time}')

    except UncorrectedInputCity as err:
        logger.error(err)
    finally:
        driver.close()
        driver.quit()


async def get_button_text_time_zone(message: Message):
    await message.answer('Введите пожалуйста свой часовой пояс в формате: ±HH:MM')

