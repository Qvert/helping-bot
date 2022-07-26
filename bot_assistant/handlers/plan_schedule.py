import asyncio
import datetime
import os
import re
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loguru import logger

from bot_assistant.keyboard import keyboard_plan
from bot_assistant.state_class.class_state import Scheduler_plan
from bot_assistant.utils_.class_error import UncorrectedInputCity, NoTimeUser
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
    zone_time = get_time_zone(text_city := message.text)
    if zone_time is None:
        await message.reply('Ой 😟, кажется вы допустили ошибку в написаний города.')
        return

    logger.debug(f'{text_city}: time_zone {zone_time}')

    db.update_data_base(data='time_zone', value=zone_time[3:5], id_us=message.from_user.id)

    logger.debug('Update zone_time succsefull')
    await message.answer(f'Ваш часовой пояс установлен на: {zone_time}')
    await message.answer(f'Теперь вы можете использовать планировщика')
    await asyncio.sleep(2)
    await message.answer(f'Для этого введите сначала событие, а потом ')
    await state.finish()


async def get_button_text_time_zone(message: Message):
    await message.answer('⚠ Небольшая подсказка по введению часовго пояса!!! ⚠\n'
                         '1. Вводить нужно относительно 00:00 и в формате ±H:00.\n'
                         '2. Можете посмотреть свой часовой пояс на сайте https://www.timeserver.ru\n'
                         '3. Для примера: у Москвы будет часовой пояс, отноcительно 00:00, +3:00\n'
                         'Удачного использования планировщика 👋')

    await Scheduler_plan.time_zone_user.set()


async def get_text_input_user(message: Message, state: FSMContext):
    text_input_user = message.text

    logger.info(f'Input text user: {text_input_user}')

    db.update_data_base(data='time_zone', value=text_input_user, id_us=message.from_user.id)
    logger.debug('Update zone_time succsefull')
    await message.answer(f'Ваш часовой пояс установлен на: {text_input_user}')
    await message.answer(f'Теперь вы можете использовать планировщика')
    await asyncio.sleep(2)
    await message.answer(f'Для того чтобы записать событие используйте запись типа:\n'
                         f'[Событие] [Время в формате HH:MM] [Через сколько времени должно случится событие]')
    await Scheduler_plan.get_plan_to_user.set()


async def get_plan_to_user_(message: Message):
    """
    :param message: Обработик сообщений
    :return: Получаем план пользователя и обрабатываем его
    """
    text_user = message.text
    logger.debug(f'Text plan for user {text_user}')
    try:
        time_user = re.search(r'\d\d:\d\d', text_user)
        if time_user is None:
            await message.reply('Пожалуйста проверьте правильность написания времени')
            raise NoTimeUser

        split_text_user = text_user.split(time_user[0])
        logger.info(f'{split_text_user = }\n'
                    f'{time_user = }')

        # Добавляем в базу данных событие, которое случится у пользоватл\еля
        db.update_data_base(data='event', value=split_text_user[0], id_us=message.from_user.id)
        time_zone = db.get_data_base(data='time_zone', id_us=message.from_user.id)[0][0]
        logger.info(f'Get time user: {time_zone}')
        date_today = datetime.datetime.today()
        date_today += datetime.timedelta(hours=int(time_zone[1]))

        db.update_data_base(data='start_time', value=date_today.strftime("%Y-%m-%d-%H.%M.%S"),
                            id_us=message.from_user.id)
        logger.debug(f'Start from time: {date_today}')

        # Текст, когда должно случиться событие
        text_end_time = split_text_user[1]
        logger.info(f'Info end time: {text_end_time}')

    except NoTimeUser as err:
        logger.error(err)
        await message.reply('Пожалуйста проверьте правильность написания')


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
