import asyncio
from string import Template
import os

import pyowm.commons.exceptions
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from pyowm import OWM
from loguru import logger

from bot_assistant.state_class.class_state import Weather


async def weather(message: Message) -> None:
    """
    :param message: Message
    :return: Вход в состояние вопроса населённого пункта
    """
    await message.answer('Введите пожалуйста населённый пункт где хотите узнать погоду')
    await Weather.get_weather_place.set()


async def get_weather_text(message: Message, state: FSMContext):
    """
    :param message: Message
    :param state: FSMContext
    :return: Обработка погоды и отправка пользователю
    """
    weather_place = message.text
    try:
        owm = OWM(os.environ['TOKEN_OWM'])
        mgr = owm.weather_manager().weather_at_place(weather_place).weather
        await message.answer(f'Сейчас минуточку')
        await asyncio.sleep(2)
        stroke = Template('Вот что мне удалось найти\n\n'
                          'Сейчас в $place:\n'
                          'Температура максимальная: $temp_max °C\n'
                          'Температура средняя: $temp °C\n'
                          'Температура минимальная: $temp_min °C\n'
                          'Скорость ветра: $wind м/c\n'
                          'Влажность: $hum%\n'
                          '')\
            .safe_substitute(place=weather_place, temp=mgr.temperature('celsius')['temp'],
                             temp_max=mgr.temperature('celsius')['temp_max'],
                             temp_min=mgr.temperature('celsius')['temp_min'],
                             wind=mgr.wind()['speed'],
                             hum=mgr.humidity)

    except pyowm.commons.exceptions.NotFoundError as err:
        await message.reply('Пожалуйста проверьте правильность написания.')
        logger.error(err)
    finally:
        await message.answer(stroke)

    await state.finish()

