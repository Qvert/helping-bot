from __future__ import annotations
import datetime
from datetime import timedelta

import asyncio
import typing as ty

from aiogram import types
from aiogram.types import Message
from loguru import logger

from bot_assistant.utils_.class_error import DontWritePlan
from bot_assistant.database.ex_db import db


async def send_message(message: Message, time_rem: str, event: str, time_end: str) -> None:
    """
    :param message: Message
    :param time_rem: Промежуток времени напоминания
    :param event: Событие
    :param time_end: Дата окончания
    :return:
    """
    time_end_str = time_end
    time_end_time = [int(el) for el in time_end_str[-1].split('.')]

    time_end_datetime = datetime.datetime(year=int(time_end_str[0]), month=int(time_end_str[1]),
                                          day=int(time_end_str[2]),
                                          hour=time_end_time[0], minute=time_end_time[1])
    logger.info(f'Time end: {time_end_datetime}')

    date_now = datetime.datetime.today()
    date_now += timedelta(hours=int(db.get_data_base(data='time_zone',
                                                     id_us=message.from_user.id)[0][0][1]))
    logger.info(f'Date now bot: {date_now}')

    while True:
        await asyncio.sleep(int(time_rem))
        await message.answer(f'📢 <b>Напоминаю</b>, что у вас запланировано событие: {event}\n'
                             f'<b>Дата свершения:</b> {time_end}', parse_mode=types.ParseMode.HTML)

        if (time_end_datetime - date_now).total_seconds() < 0:
            await message.answer(f'Удаляю событие: {event}, так как оно уже свершилось')
            break


async def main() -> ty.NoReturn:
    while True:
        await asyncio.gather()


async def pooling(message: Message, time_rem: str, event: str, time_end: str) -> None:
    try:
        if time_rem and event is not None:
            asyncio.create_task(send_message(message=message, time_rem=time_rem, event=event, time_end=time_end))
            await message.answer('Ваша запись успешно добавлена, ожидайте напоминания)')

    except DontWritePlan as err:
        logger.error(err)
        await message.answer('Простите, случилась непредвиденная ошибка(')


