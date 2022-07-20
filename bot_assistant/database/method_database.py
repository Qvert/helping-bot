from .connected_to_database import connection
from string import Template
from loguru import logger


class UsersData:
    def __init__(self):
        """
        Подключение к базе данных
        """
        self.connection = connection
        self.cursor = self.connection.cursor()

    def get_data_base(self, data: str) -> tuple:
        """
        :param data: Значение, которое хотим получить
        :return: Кортеж со значениями
        """
        stroka_zap = Template(
            "SELECT $data FROM users;"
        ).safe_substitute(
            data=data
        )
        with self.connection:
            self.cursor.execute(
                stroka_zap
            )
            result = self.cursor.fetchall()[0]
            connection.commit()
            logger.debug(f'Get user_id from database {result}')
            return result

    def update_data_base(self, data: str, value: str) -> None:
        """
        :param data: Наименование поля в таблице базы данных
        :param value: Значение, которое хотим вставить
        :return: None
        """
        pass

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