from bot_assistant.database.method_database import UsersData

db = UsersData()


def generate_stroka_database(data_from_bd: str, value: str, id_user: str) -> None:
    """
    :param value: То, что нужно вставить в бд.
    :param data_from_bd: Параметр в базе данных.
    :param id_user: Айди пользователя.
    :return: Добавляем строку в базу.
    """
    data_user = db.get_data_base(data=data_from_bd, id_us=id_user)[0][0]

    if data_user is not None:
        list_event = data_user.split(', ')
        list_event.append(value)
        db.update_data_base(data=data_from_bd, value=', '.join(list_event), id_us=id_user)

    else:
        db.update_data_base(data=data_from_bd, value=value, id_us=id_user)