from __future__ import annotations

import asyncio
import typing as ty

from aiogram.types import Message


async def send_message(message: Message, time_rem: str, event: str) -> None:
    while True:
        await asyncio.sleep(int(time_rem))
        await message.answer(f'У вас событие: {event}')


async def main() -> ty.NoReturn:
    while True:
        await asyncio.gather(pooling())


async def pooling(message: Message, time_rem: str, event: str) -> None:
    if time_rem and event is not None:
        asyncio.create_task(send_message(message=message, time_rem=time_rem, event=event))