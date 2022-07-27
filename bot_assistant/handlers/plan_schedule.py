import asyncio
import datetime
import re

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loguru import logger

from bot_assistant.keyboard import keyboard_plan
from bot_assistant.state_class.class_state import Scheduler_plan
from bot_assistant.utils_.class_error import NoTimeUser
from bot_assistant.database.method_database import UsersData
from bot_assistant.utils_.dict_get import dict_plan_number_time, dict_plan_number_time_week, dict_next_day
from bot_assistant.utils_.selenium_parse import get_time_zone

db = UsersData()


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
    await message.answer('Сейчас мы установим ваш часовой пояс, пожалуйста ждите.')
    zone_time = get_time_zone(text_city := message.text)
    if zone_time is None:
        await message.reply('Ой 😟, кажется вы допустили ошибку в написаний города.')
        return

    logger.debug(f'{text_city}: time_zone {zone_time}')

    db.update_data_base(data='time_zone', value=zone_time[3:5], id_us=message.from_user.id)

    logger.debug('Update zone_time succsefull')
    await message.answer(f'Ваш часовой пояс установлен на: {zone_time}')
    await message.answer(f'Теперь вы можете использовать планировщика')
    await asyncio.sleep(2)
    await message.answer(f'Для этого введите сначала событие, а потом ')
    await state.finish()


async def get_button_text_time_zone(message: Message):
    await message.answer('⚠ Небольшая подсказка по введению часовго пояса!!! ⚠\n'
                         '1. Вводить нужно относительно 00:00 и в формате ±H:00.\n'
                         '2. Можете посмотреть свой часовой пояс на сайте https://www.timeserver.ru\n'
                         '3. Для примера: у Москвы будет часовой пояс, отноcительно 00:00, +3:00\n'
                         'Удачного использования планировщика 👋')

    await Scheduler_plan.time_zone_user.set()


async def get_text_input_user(message: Message, state: FSMContext):
    text_input_user = message.text

    logger.info(f'Input text user: {text_input_user}')

    db.update_data_base(data='time_zone', value=text_input_user, id_us=message.from_user.id)
    logger.debug('Update zone_time succsefull')
    await message.answer(f'Ваш часовой пояс установлен на: {text_input_user}')
    await message.answer(f'Теперь вы можете использовать планировщика')
    await asyncio.sleep(2)
    await message.answer(f'Для того чтобы записать событие используйте запись типа:\n'
                         f'[Событие] [Время в формате HH:MM] [Через сколько времени должно случится событие]')
    await Scheduler_plan.get_plan_to_user.set()


async def get_plan_to_user_(message: Message):
    """
    :param message: Обработик сообщений
    :return: Получаем план пользователя и обрабатываем его
    """
    text_user = message.text
    logger.debug(f'Text plan for user {text_user}')
    try:
        time_user = re.search(r'\d\d:\d\d', text_user)[0]
        if time_user is None:
            await message.reply('Пожалуйста проверьте правильность написания времени')
            raise NoTimeUser

        split_text_user = text_user.split(time_user)
        logger.info(f'{split_text_user = }\n'
                    f'{time_user = }')

        # Добавляем в базу данных событие, которое случится у пользоватл\еля
        db.update_data_base(data='event', value=split_text_user[0], id_us=message.from_user.id)
        time_zone = db.get_data_base(data='time_zone', id_us=message.from_user.id)[0][0]
        logger.info(f'Get time user: {time_zone}')
        date_today = datetime.datetime.today()
        date_today += datetime.timedelta(hours=int(time_zone[1]))

        db.update_data_base(data='start_time', value=date_today.strftime("%Y-%m-%d-%H.%M.%S"),
                            id_us=message.from_user.id)
        logger.debug(f'Start from time: {date_today}')

        # Текст, когда должно случиться событие
        text_end_time = split_text_user[1].strip()
        logger.info(f'Info end time: {text_end_time}')
        time_user_end = time_user.split(':')

        date_end_str = datetime.datetime(date_today.year, date_today.month, date_today.day,
                                         int(time_user_end[0]), int(time_user_end[1]))
        logger.info(f'{date_end_str = }')

        if 'через' in text_end_time:
            split_char_time = text_end_time.split()[1:]
            logger.info(f'{split_char_time = }')

            number_time = split_char_time[0]
            logger.info(f'{number_time = }')
            # If user input day
            if len(number_days_or_week := split_char_time[-1]) == 3 or len(number_days_or_week) == 4:
                date_end_str = handler_time(date_end_str=date_end_str, number_time=number_time, days_week_month='day')

            elif len(number_days_or_week) == 6 and 'недел' in number_days_or_week:
                date_end_str = handler_time(date_end_str=date_end_str, number_time=number_time, days_week_month='week')

            '''elif len(number_days_or_week) >= 5 and 'месяц' in number_days_or_week:
                date_end_str = handler_time(date_end_str=date_end_str, number_time=number_time, days_week_month='month')'''

        elif len(text_end_time.split()) == 1:
            date_end_str += datetime.timedelta(days=dict_next_day[text_end_time])

        db.update_data_base(data='end_time', value=date_end_str,
                            id_us=message.from_user.id)

    except NoTimeUser as err:
        logger.error(err)
        await message.reply('Пожалуйста проверьте правильность написания')


def handler_time(number_time: str, date_end_str: datetime, days_week_month: str) -> str:
    """
    :param number_time: Промежуток во времени
    :param date_end_str: Дата, когда должно случится событие
    :param days_week_month: Условие, через день, месяц, недели произойдёт событие
    :return: Дата, когда случится событие
    """
    if days_week_month == 'day':
        if len(number_time) == 1:
            date_end_str += datetime.timedelta(days=int(number_time))
            return date_end_str.strftime("%Y-%m-%d-%H.%M.%S")
        else:
            date_end_str += datetime.timedelta(days=dict_plan_number_time[number_time])
            return date_end_str.strftime("%Y-%m-%d-%H.%M.%S")

    if days_week_month == 'week':
        if len(number_time) == 1:
            date_end_str += datetime.timedelta(weeks=int(number_time))
            return date_end_str.strftime("%Y-%m-%d-%H.%M.%S")
        else:
            date_end_str += datetime.timedelta(weeks=dict_plan_number_time_week[number_time])
            return date_end_str.strftime("%Y-%m-%d-%H.%M.%S")

    '''if days_week_month == 'month':
        if len(number_time) == 1:
            date_end_str += datetime.timedelta(=int(number_time))
            return date_end_str
        else:
            date_end_str += datetime.timedelta(weeks=dict_plan_number_time[number_time])
            return date_end_str
'''
