from string import Template
import os

import pyowm.commons.exceptions
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from pyowm import OWM
from loguru import logger

from bot_assistant.state_class.class_state import Weather
from bot_assistant.keyboard import keyboard_cancel


async def weather(message: Message) -> None:
    """
    :param message: Message
    :return: Вход в состояние вопроса населённого пункта
    """
    await message.answer('Теперь можешь мне сказать🗣️ в каком месте нужно узнать погоду ☁️',
                         reply_markup=keyboard_cancel)
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
        stroke = Template('Вот что мне удалось найти\n\n'
                          'Сейчас в $place:\n'
                          '🌡 Температура:\n'
                          '    Максимальная: $temp_max °C\n'
                          '    Средняя: $temp °C\n'
                          '    Минимальная: $temp_min °C\n'
                          '💨 Скорость ветра: $wind м/c\n'
                          '🌧 Влажность: $hum%\n'
                          '')\
            .safe_substitute(place=weather_place, temp=mgr.temperature('celsius')['temp'],
                             temp_max=mgr.temperature('celsius')['temp_max'],
                             temp_min=mgr.temperature('celsius')['temp_min'],
                             wind=mgr.wind()['speed'],
                             hum=mgr.humidity)

        await message.answer(stroke)

    except pyowm.commons.exceptions.NotFoundError as err:
        await message.reply('Не могу разобрать 🧐 напиши понятнее 🖊️')
        logger.error(err)

    await state.finish()

