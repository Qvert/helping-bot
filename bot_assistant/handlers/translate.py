from aiogram.types import Message
from aiogram.dispatcher import FSMContext
import googletrans
from deep_translator import GoogleTranslator

from loguru import logger

from bot_assistant.keyboard import keyboard_translate, keyboard_review
from bot_assistant.state_class.class_state import TranslateClass


async def post_quastion_language(message: Message):
    await message.answer('Вы решили воспользоваться переводчиком\n'
                         'Для этого выберите сначала язык на который хотите перевести текст',
                         reply_markup=keyboard_translate)
    await TranslateClass.get_from_language.set()


async def get_language_user(message: Message, state: FSMContext):
    language = message.text
    logger.info(f'{language = }')

    await state.update_data(lan=language)
    await message.answer(f'Теперь введите текст, который нужно перевести', reply_markup=keyboard_review)
    await TranslateClass.get_text_translate.set()


async def get_text_translate(message: Message, state: FSMContext):
    await state.update_data(text_trans=message.text)
    text_language = await state.get_data()
    translated = GoogleTranslator(source='auto',
                                  target='en').translate(text_language['lan'].lower()).lower()
    logger.info(f'language trans {translated = }')
    translate_text_user = GoogleTranslator(source='auto',
                                           target=googletrans.LANGCODES[translated]).\
        translate(text_language['text_trans'])

    await message.answer(translate_text_user)
    await state.finish()





