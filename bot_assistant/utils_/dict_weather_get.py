from types import MappingProxyType

dict_plan_number_time = MappingProxyType({
    'один': 1,
    'два': 2,
    'три': 3,
    'четыре': 4,
    'пять': 5,
    'шесть': 6,
    'семь': 7,
    'восемь': 8,
    'девять': 9,
    'десять': 10,
})

dict_plan_number_time_week = MappingProxyType({
    'одну': 1,
    'две': 2,
    'три': 3,
    'четыре': 4,
    'пять': 5,
    'шесть': 6,
    'семь': 7,
    'восемь': 8,
    'девять': 9,
    'десять': 10,
})

dict_next_day = MappingProxyType(
    {
        'завтра': 1,
        'послезавтра': 2,
        'послепослезавтра': 3,
        'сегодня': 0,
    }
)

