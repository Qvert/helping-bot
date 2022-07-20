from loguru import logger
import psycopg2
import os


connection = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')

'''with connection.cursor() as cursor:
    cursor.execute(
        "CREATE TABLE users ("
        "id_user INT,"
        "time_zone VARCHAR,"
        "start_time VARCHAR,"
        "end_time VARCHAR,"
        "event VARCHAR,"
        "reminder_time VARCHAR);"
    )
    connection.commit()'''
'''with connection.cursor() as cursor:
    cursor.execute(
        'DROP TABLE users'
    )
    connection.commit()'''

