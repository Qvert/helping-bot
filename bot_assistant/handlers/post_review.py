import random
import os
import vk_api

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from bot_assistant.keyboard import keyboard_cancel, keyboard_review
from bot_assistant.state_class.class_state import Review

vk_session = vk_api.VkApi(token=os.environ['TOKEN_VK'])
vk = vk_session.get_api()


async def review(message: Message):
    await message.answer('💬 Оставь коммент👇на счет меня какой я был полезный👍 и крутым 🤘,\n'
                         'И можешь мне подсказать по дружески что во мне не хватает😏,\n'
                         'А я потом буду еще лучше для тебя 😎 , чтобы тебе помочь как твой лучший друг 😋 .',
                         reply_markup=keyboard_cancel)
    await Review.waiting_text_review.set()


async def review_get_text(message: Message, state: FSMContext):
    """
    :param message: Message
    :param state: FSMContext
    :return: Отправляет отзыв на почту разработчику
    """
    text_review = message.text
    vk.messages.send(peer_id=os.environ['USER_ID'], message=f'Пользователь {message.from_user.full_name}\n'
                                                            f'Отправил отзыв: {text_review}',
                     random_id=random.randint(-2147483648, +2147483648))
    await message.answer(f'Отзыв успешно отправлен)\n'
                         f'Спасибо за поддержку', reply_markup=keyboard_review)
    await state.finish()