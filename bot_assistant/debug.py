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
import time
import asyncio

database = ['Пойти гулять', 'поесть']
time_ = [5, 10]


async def foo(remider, event):
    while True:
        await asyncio.sleep(remider)
        print(event)

ioloop = asyncio.get_event_loop()

event1 = ioloop.create_task(foo(remider=time_[0], event=database[0]))
# event2 = ioloop.create_task(foo(remider=time_[1], event=database[1]))
tasks = [event1]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()
