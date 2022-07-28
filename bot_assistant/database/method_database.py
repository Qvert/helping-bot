from bot_assistant.database.connected_to_database import connection
from string import Template
from loguru import logger


class UsersData:
    def __init__(self):
        """
        Подключение к базе данных
        """
        self.connection = connection
        self.cursor = self.connection.cursor()

    def get_data_base(self, data: str, id_us: str) -> tuple:
        """
        :param id_us: Айди пользователя в телеграмм
        :param data: Значение, которое хотим получить
        :return: Кортеж со значениями
        """
        stroka_zap = Template(
            "SELECT $data FROM users WHERE id_user = $id_us;"
        ).safe_substitute(
            data=data,
            id_us=id_us,
        )
        with self.connection:
            self.cursor.execute(
                stroka_zap
            )
            result = self.cursor.fetchall()
            connection.commit()
            logger.debug(f'Get {data} from database {result}')
            return result

    def update_data_base(self, data: str, value: str, id_us: str) -> None:
        """
        :param id_us: Айдишник пользователя
        :param data: Наименование поля в таблице базы данных
        :param value: Значение, которое хотим вставить
        :return: None
        """
        stroka_zap = Template(
            "UPDATE users SET $data = '$value' "
            "WHERE id_user = '$id';"
        ).safe_substitute(
            data=data,
            value=value,
            id=id_us
        )
        with self.connection:
            self.cursor.execute(
                stroka_zap
            )
            logger.info(f'Database update done !!!')
            self.connection.commit()

    def insert_data_to_base(self, data: str, value: str) -> None:
        """
        :param data: Наименование поля в базе
        :param value: Значение, которое нужно вставить
        :return: None
        """
        stroka_zap = Template(
            "INSERT INTO users ($id) VALUES ($val);"
        ).safe_substitute(id=data, val=value)

        with self.connection:
            self.cursor.execute(
                stroka_zap
            )
            logger.info(f'Insert {value} to {data} succesfull')
            self.connection.commit()