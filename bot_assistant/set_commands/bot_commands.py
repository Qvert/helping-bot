from aiogram.types import BotCommand


async def set_commands(dis):
    """
    :param dis: Dispatcher
    :return: Создаем меню с командами чат бота
    """
    commands = [
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/weather", description="Узнать погоду"),
        BotCommand(command="/plan", description="Планировщик"),
        BotCommand(command="/translate", description="Переводчик"),
        BotCommand(command="/search", description="Поиск информаций"),
        BotCommand(command="/music", description="Поиск и отправка музыки")
    ]
    await dis.bot.set_my_commands(commands)