from aiogram.dispatcher.filters.state import State, StatesGroup


class Review(StatesGroup):
    """
    Класс для взятие отзыва
    """
    waiting_text_review = State()


class Weather(StatesGroup):
    """
    Класс для взятия места, на котором нужно узнать погоду
    """
    get_weather_place = State()


class GetNameMusic(StatesGroup):
    """
    Класс, в котором принимается название музыки иrl
    """
    music_name = State()
    url_music = State()


class TranslateClass(StatesGroup):
    """
    Класс для принятия языка и текста перевода
    """
    get_from_language = State()
    get_text_translate = State()


class SearchEthernet(StatesGroup):
    """
    Класс с состоянием поиска
    """
    text_search = State()


class Scheduler_plan(StatesGroup):
    """
    Класс для планировщика
    """
    get_name_city = State()
    time_zone_user = State()
    get_plan_to_user = State()
