import datetime

date = datetime.datetime.today()
date_today = date.strftime("%Y-%m-%d-%H-%M-%S")
date = [int(el) for el in date_today.split('-')]

print(datetime.datetime(year=date[0],
                        month=date[1],
                        day=date[2],
                        hour=date[3],
                        minute=date[4],
                        second=date[5]).hour)
