from scripts.services import SERVICES
import sqlite3
import datetime
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

log_base = config['FILES']['LOG_BASE']
error_base = config['FILES']['ERROR_BASE']


def log_write(message):
    if message.chat.type != 'channel':
        if str(message.from_user.id) == '126017510':
            return

    text = message.text.replace('\n', ' ').strip().split(' ')[-1]

    service = ''
    for key in list(SERVICES.keys()):
        if SERVICES[key]['link'] in text:
            service = key
            break

    chat_type = message.chat.type
    user_id = str(message.chat.id) if chat_type == 'channel' else str(
        message.from_user.id)
    username = message.chat.username if chat_type == 'channel' else message.from_user.username
    first_name = message.chat.title if chat_type == 'channel' else message.from_user.first_name
    last_name = message.author_signature if chat_type == 'channel' else message.from_user.last_name
    chat_id = message.chat.id if chat_type == 'group' or chat_type == 'supergroup' else 'None'
    chat_title = message.chat.title if chat_type == 'group' or chat_type == 'supergroup' else 'None'
    language = 'None' if chat_type == 'channel' else message.from_user.language_code
    time = datetime.datetime.fromtimestamp(
        message.date).strftime("%Y-%m-%d %H:%M:%S")

    to_log = [chat_type, user_id, username, first_name, last_name,
              chat_id, chat_title, language, time, service, text]

    to_log_base_write(to_log)


def to_log_base_write(log_object):
    with sqlite3.connect(log_base) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO logs VALUES (:type, :user_id, :username, :first_name, :last_name, :chat_id, :chat_title, :language, :time, :service, :query)",
                       {
                           'type': log_object[0],
                           'user_id': log_object[1],
                           'username': log_object[2],
                           'first_name': log_object[3],
                           'last_name': log_object[4],
                           'chat_id': log_object[5],
                           'chat_title': log_object[6],
                           'language': log_object[7],
                           'time': log_object[8],
                           'service': log_object[9],
                           'query': log_object[10]
                       }
                       )
        connection.commit()


def error_write(message, error):
    with sqlite3.connect(error_base) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO errors VALUES (:message, :error)", {
                       'message': str(message), 'error': str(error)})
        connection.commit()
