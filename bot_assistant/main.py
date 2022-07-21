import os

from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from art import *

from database.method_database import UsersData
from handlers.loading_music import post_music, get_name_music, load_music
from handlers.plan_schedule import welcome_message, get_button_text_city, get_button_text_time_zone, city_input_user
from handlers.post_review import review, review_get_text
from handlers.search_method import get_text_search, post_get_search
from handlers.translate import post_quastion_language, get_language_user, get_text_translate
from handlers.weather import weather, get_weather_text
from keyboard import keyboard_review
from state_class.class_state import Weather, Review, GetNameMusic, TranslateClass, SearchEthernet, Scheduler_plan

# Connected to bot
bot = Bot(token=os.environ['BOT_TOKEN'])
dis = Dispatcher(bot, storage=MemoryStorage())

# Connected to database
db = UsersData()


@dis.message_handler(commands='start')
async def test_message(message: types.Message):
    if message.from_user.id not in db.get_data_base(data='id_user'):
        db.insert_data_to_base(data='id_user', value=message.from_user.id)

    await message.answer('Хай👋 ! Я Assistant, ознакомься с тем что я могу.\n'
                         'Чтобы узнать обо мне 🧐 или что я могу 😋 просто напиши или нажми /help',
                         reply_markup=keyboard_review)


@dis.message_handler(commands='help')
async def welcome_message_start(message: types.Message):
    await message.answer('Этому боту доступен следующий функционал\n'
                         'Вывод погоды: /weather\n'
                         'Создание планировщика с напоминанием: /plan\n'
                         'Перевод на большинство языков: /translate\n'
                         'Поиск информаций: /search\n'
                         'Возможность отправлять музыку: /music')


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


if __name__ == '__main__':
    tprint('coffee stain', font='random')
    # set_commands(dis)
    register_hundlers(dis)
    executor.start_polling(dis, skip_updates=True)
