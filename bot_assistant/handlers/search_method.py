from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loguru import logger
from googlesearch import search

from bot_assistant.state_class.class_state import SearchEthernet
from bot_assistant.keyboard import keyboard_cancel


async def get_text_search(message: Message):
    await message.answer('Можешь написать ✍ что тебе надо найти 🧐', reply_markup=keyboard_cancel)
    await SearchEthernet.text_search.set()
    logger.debug('Next func post_get_search')


async def post_get_search(message: Message, state: FSMContext):
    """ TODO: Сделать настраиваемое количество показываемых ссылок"""
    text_message_search = message.text
    list_search = search(text_message_search, stop=7)
    logger.debug(f'{list_search = }')
    await message.reply('Я нашёл то что вы хотели 🤓')

    if list_search is None:
        await message.answer('Я не смог найти 😅 ответ на твой вопрос 😞')
    for _url in list_search:
        await message.answer(_url)
    logger.info('Operation search Ok!!')
    await state.finish()

