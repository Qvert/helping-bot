import asyncio
import os

from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from art import *

from handlers.loading_music import post_music, get_name_music, load_music
from handlers.plan_schedule import welcome_message, get_button_text_city, get_button_text_time_zone, city_input_user, \
    get_text_input_user, get_plan_to_user_, post_reminder_time
from handlers.post_review import review, review_get_text
from handlers.search_method import get_text_search, post_get_search
from handlers.translate import post_quastion_language, get_language_user, get_text_translate
from handlers.weather import weather, get_weather_text
from keyboard import keyboard_review
from state_class.class_state import Weather, Review, GetNameMusic, TranslateClass, SearchEthernet, Scheduler_plan
from bot_assistant.database.method_database import UsersData


# Connected to bot
bot = Bot(token=os.environ['BOT_TOKEN'])
dis = Dispatcher(bot, storage=MemoryStorage())


db = UsersData()


@dis.message_handler(commands='start')
async def test_message(message: types.Message):
    if message.from_user.id not in db.get_data_base(data='id_user', id_us=message.from_user.id):
        db.insert_data_to_base(data='id_user', value=message.from_user.id)

    await message.answer('Хай👋 ! Я Assistant, ознакомься с тем что я могу.\n'
                         'Чтобы узнать обо мне 🧐 или что я могу 😋 просто напиши или нажми /help',
                         reply_markup=keyboard_review)


@dis.message_handler(commands='help')
async def welcome_message_start(message: types.Message):
    await message.answer('⬇ <b>Общие сведения по использованию данного чат-бота</b> ⬇\n\n'
                         '1. ⛅ <b>Функция "Узнать погоду": /weather.</b>\n'
                         '   <b>1.1.</b> Для того чтобы узнать погоду там, где вы\n'
                         '               находитесь нужно ввести либо город, либо населённый пункт где вы находитесь.\n\n'
                         '   <b>1.2.</b> Вы можете в любой момент отменить действие и выбрать уже другую функцию.\n'
                         '               Для этого появится специальная кнопка.\n\n'
                         '2. 📔 <b>Функция "Планировщик": /plan.</b>\n'
                         '   <b>2.1</b> Позволяет вам не запоминать события, которые должны пройзоити.\n'
                         '              Вместо этого программа сама будет напоминать вам о том, что должно случиться\n\n'
                         '   <b>2.2</b> Вначале использование, вам нужно будет указать свой часовой пояс.\n'
                         '              Это нужно для того, чтобы программа выводила напоминание в правильное время\n'
                         '              Чтобы его указать, вам будет предоставлен выбор из двух кнопок\n'
                         '              (Указать самому, либо автоматически определить)\n\n'
                         '   <b>2.3</b> Событие должно вводится строго в таком формате\n'
                         '              [Событие] [Время в HH:MM] [Когда должно пройзоити(сегодня, через 2 дня)]\n\n'
                         '   <b>2.4</b> Вы можете в любой момент изменить часовой пояс.\n'
                         '              Для этого будет предоставлена специальная команда.\n\n'
                         '3. <b>Функция "Переводчик": /translate</b>\n', parse_mode=types.ParseMode.HTML)


@dis.message_handler(Text(equals='❌ Отмена', ignore_case=True), state='*')
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('🚫 Отменено', reply_markup=keyboard_review)


# Инлайн кнопка и её обработка
'''@dis.message_handler(commands='random')
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Нажми меня', callback_data='random_value'))
    await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10", reply_markup=keyboard)


@dis.callback_query_handler(text='random_value')
async def send_random_value(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer(str(random.randint(0, 10)))'''


def register_hundlers(dis: Dispatcher):
    dis.register_message_handler(weather, commands='weather', state='*')
    dis.register_message_handler(get_weather_text, state=Weather.get_weather_place)
    dis.register_message_handler(review, Text(equals='💬 Оставить отзыв 💬', ignore_case=True), state='*')
    dis.register_message_handler(review_get_text, state=Review.waiting_text_review)
    dis.register_message_handler(get_name_music, commands='music', state='*')
    dis.register_message_handler(post_music, state=GetNameMusic.music_name)
    dis.register_message_handler(load_music, state=GetNameMusic.url_music)
    dis.register_message_handler(post_quastion_language, commands='translate', state='*')
    dis.register_message_handler(get_language_user, state=TranslateClass.get_from_language)
    dis.register_message_handler(get_text_translate, state=TranslateClass.get_text_translate)
    dis.register_message_handler(get_text_search, commands='search', state='*')
    dis.register_message_handler(post_get_search, state=SearchEthernet.text_search)
    dis.register_message_handler(welcome_message, commands='plan', state='*')
    dis.register_message_handler(get_button_text_city, Text(equals='🏙 Ввести мой город', ignore_case=True), state='*')
    dis.register_message_handler(get_button_text_time_zone, Text(equals='⌨ Написать самому',
                                                                 ignore_case=True), state='*')
    dis.register_message_handler(city_input_user, state=Scheduler_plan.get_name_city)
    dis.register_message_handler(get_text_input_user, state=Scheduler_plan.time_zone_user)
    dis.register_message_handler(get_plan_to_user_, state=Scheduler_plan.get_plan_to_user)
    dis.register_message_handler(post_reminder_time, state=Scheduler_plan.reminder_time_user)


if __name__ == '__main__':
    tprint('coffee stain', font='random')
    # set_commands(dis)
    register_hundlers(dis)
    executor.start_polling(dis, skip_updates=True)

    from utils_.asyncio_polling import main
    asyncio.run(main())
