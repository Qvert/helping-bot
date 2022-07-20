from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loguru import logger
from googlesearch import search

from bot_assistant.state_class.class_state import SearchEthernet


async def get_text_search(message: Message):
    await message.answer('Что вы хотите найти?)')
    await SearchEthernet.text_search.set()
    logger.debug('Next func post_get_search')


async def post_get_search(message: Message, state: FSMContext):
    """ TODO: Сделать настраиваемое количество показываемых ссылок"""
    text_message_search = message.text
    list_search = search(text_message_search, stop=7)
    logger.debug(f'{list_search = }')
    await message.reply('Вот что удалось мне найти')

    if list_search is None:
        await message.answer('Извините, но ничего не удалось найти по этому вопросу(')
    for _url in list_search:
        await message.answer(_url)
    logger.info('Operation search Ok!!')
    await state.finish()

