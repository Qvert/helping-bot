import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from geopy import geocoders
from loguru import logger

from bot_assistant.keyboard import keyboard_plan
from bot_assistant.state_class.class_state import Scheduler_plan
from bot_assistant.utils_.class_error import UncorrectedInputCity


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
    try:
        city_or_country = message.text
        g = geocoders.GoogleV3()
        place, (lat, lng) = g.geocode(city_or_country)
        timezone = g.timezone((lat, lng))

    except UncorrectedInputCity as err:
        await message.reply('Введите пожалуйста корректное название города или населённого пункта')
        logger.error(err)


async def get_button_text_time_zone(message: Message):
    await message.answer('Введите пожалуйста свой часовой пояс в формате: ±HH:MM')

