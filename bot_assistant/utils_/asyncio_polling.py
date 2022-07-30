from __future__ import annotations

import asyncio
import typing as ty

from aiogram import types
from aiogram.types import Message
from loguru import logger

from bot_assistant.utils_.class_error import DontWritePlan


async def send_message(message: Message, time_rem: str, event: str, time_end: str) -> None:
    while True:
        await asyncio.sleep(int(time_rem))
        await message.answer(f'📢 <b>Напоминаю</b>, что у вас запланировано событие: {event}\n'
                             f'<b>Дата свершения:</b> {time_end}', parse_mode=types.ParseMode.HTML)


async def main() -> ty.NoReturn:
    while True:
        await asyncio.gather(pooling())


async def pooling(message: Message, time_rem: str, event: str, time_end: str) -> None:
    try:
        if time_rem and event is not None:
            asyncio.create_task(send_message(message=message, time_rem=time_rem, event=event, time_end=time_end))
            await message.answer('Ваша запись успешно добавлена, ожидайте напоминания)')

    except DontWritePlan as err:
        logger.error(err)
        await message.answer('Простите, случилась непредвиденная ошибка(')


