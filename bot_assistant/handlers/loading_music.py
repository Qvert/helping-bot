import requests
import os

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile
from loguru import logger
import undetected_chromedriver
from bs4 import BeautifulSoup
from undetected_chromedriver import ChromeOptions

from bot_assistant.state_class.class_state import GetNameMusic


async def get_name_music(message: Message):
    await message.answer('Введите пожалуйста название музыки))')
    await GetNameMusic.music_name.set()


async def post_music(message: Message, state: FSMContext):
    logger.debug(f'{message.text =}')
    content = await searchmusic(message.text)
    logger.debug(f'{content = }')
    '''stroka_name = ''
    for i, name in enumerate(name_music := content[1]):
        stroka_name += f'[{i}]: {content[2]} {name} {name_music[name]}\n'

    await state.update_data(list_name=[name for name in name_music.keys()])
    await state.update_data(url_music=content[0])'''
    file_ = InputFile('index.html')
    await message.answer_document(document=file_)
    await message.answer('Вот что мне удалось найти\n'
                         'Чтобы выбрать песню введите её номер напротив')
    await GetNameMusic.next()


async def load_music(message: Message, state: FSMContext):
    answer: int = int(message.text)
    user_music_date = await state.get_data()
    name_music_get = user_music_date['list_name'][answer]
    try:
        response = requests.get(user_music_date['url_music'][answer])
        logger.info('Starting write music')

        with open(name_music_get, 'wb') as file:
            file.write(response.content)
        logger.info('Ending write music')

        audio = InputFile(name_music_get)
        await message.answer_audio(audio=audio)
        os.remove(name_music_get)
        await state.finish()

    except Exception as err:
        print(err)


async def searchmusic(query: str) -> list and tuple:
    """
    :param query: Название композиций
    :return: Список с ссылками на скачивание песен
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.5005.134 YaBrowser/22.7.0.1842 Yowser/2.5 Safari/537.36 '
    }
    proxies = {
        'https': 'http://188.120.226.59:3128',
    }
    quotes = requests.get(f'https://ru.hitmotop.com/search?q={query}', headers=headers, proxies=proxies)
    with open('index.html', 'w', encoding='utf8') as file:
        file.write(quotes.text)
    soup = BeautifulSoup(quotes.text, 'lxml')
    logger.debug(soup.prettify())
