'''import datetime

date = datetime.datetime.today()
date_today = date.strftime("%Y-%m-%d-%H-%M-%S")
date = [int(el) for el in date_today.split('-')]

print(datetime.datetime(year=date[0],
                        month=date[1],
                        day=date[2],
                        hour=date[3],
                        minute=date[4],
                        second=date[5]).hour)
'''
from __future__ import annotations

import typing as ty
import asyncio
from aioconsole import ainput, aprint


async def task(delay: int | float, text: str) -> None:
    await asyncio.sleep(delay)
    current_task = asyncio.current_task()
    await aprint(f"{current_task.get_name()} >> {text}")


async def pooling() -> None:
    if data := await ainput('Введите задачу в таком формате "delay:text": '):
        delay, text = data.split(":", maxsplit=1)
        asyncio.create_task(task(float(delay), text))


async def main() -> ty.NoReturn:
    while True:
        await asyncio.gather(pooling())


if __name__ == "__main__":
    asyncio.run(main())