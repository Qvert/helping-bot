import datetime
from datetime import timedelta

from bot_assistant.database.ex_db import db


time_end_str = db.get_data_base(data='end_time',
                                id_us="1195216595")[0][0].split(', ')[-1].split('-')

time_end_time = [int(el) for el in time_end_str[-1].split('.')]
time_end_datetime = datetime.datetime(year=int(time_end_str[0]), month=int(time_end_str[1]),
                                      day=int(time_end_str[2]),
                                      hour=time_end_time[0], minute=time_end_time[1])

time_start = datetime.datetime.now()


print(time_end_datetime)
print(time_start)
print((time_end_datetime - time_start).total_seconds())
