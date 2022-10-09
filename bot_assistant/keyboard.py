from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_review = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_review.add('💬 Оставить отзыв 💬')

# Клавиатура для переводчика
keyboard_translate = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_translate.row(
    KeyboardButton(
        'Русский'
    ),
    KeyboardButton(
        'Английский'
    ),
    KeyboardButton(
        'Украинский'
    ),
)
keyboard_translate.row(
    KeyboardButton(
        'Японский'
    ),
    KeyboardButton(
        'Французский'
    ),
    KeyboardButton(
        'Армянский'
    ),
)
keyboard_translate.row(
    KeyboardButton(
        '❌ Отмена'
    ),
)

# Клавиатура отмены выполнения команды
keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_cancel.add('❌ Отмена')


# Клавиатура для выбора
keyboard_plan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_plan.row(
    KeyboardButton(
        '🏙 Ввести мой город'
    ),
    KeyboardButton(
        '⌨ Написать самому'
    ),
)
keyboard_plan.add(
    KeyboardButton('❌ Отмена')
)

keyboard_count_url = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_count_url.add(
    KeyboardButton(
        'Изменить кол-во ссылок '
    )
)