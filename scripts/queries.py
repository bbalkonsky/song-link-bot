import sqlite3
import configparser
import ast
from scripts.services import SERVICES

config = configparser.ConfigParser()
config.read('config.ini')

user_base = config['FILES']['USER_BASE']
log_base = config['FILES']['LOG_BASE']
error_base = config['FILES']['ERROR_BASE']


def connection_decorator(fn):
    def wrapped(*args):
        connection = sqlite3.connect(user_base)
        cursor = connection.cursor()
        query = fn(*args, cursor)
        connection.commit()
        connection.close()
        return(query)
    return wrapped


@connection_decorator
def first_connect(cursor=None):
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users(chat_id text, services text, last_serv_req, annotations)')


def create_log_bases():
    with sqlite3.connect(log_base) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS logs(type, user_id, username, first_name, last_name, chat_id, chat_title, language, time timestamp, service, query)')
        connection.commit()

    with sqlite3.connect(error_base) as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS errors(message, error)')
        connection.commit()


@connection_decorator
def get_user_services(id, cursor=None):
    query = cursor.execute("SELECT services FROM users WHERE chat_id = :id", {
                           'id': id}).fetchone()
    if query != None:
        return ast.literal_eval(query[0])
    else:
        cursor.execute("INSERT INTO users VALUES (:chat_id, :services, :last_serv_req, :annotations)",
                       {'chat_id': id, 'services': str({val: 1 for val in list(SERVICES.keys())}), 'last_serv_req': 0, 'annotations': 0})
        return {val: 1 for val in list(SERVICES.keys())}


@connection_decorator
def set_user_services(id, codes, cursor=None):
    cursor.execute("UPDATE users SET services = :services WHERE chat_id = :chat_id", {
                   'chat_id': id, 'services': str(codes)})


# @connection_decorator
# def add_new_column(name, def_value, cursor):
#     cursor.execute(
#         "ALTER TABLE users ADD COLUMN {} DEFAULT {}".format(name, def_value))


@connection_decorator
def toggle_annotations(chat_id, cursor=None):
    status = cursor.execute("SELECT annotations FROM users WHERE chat_id = :id", {
                            'id': chat_id}).fetchone()[0]
    if status == 1:
        status = 0
    else:
        status = 1
    cursor.execute("UPDATE users SET annotations = :status WHERE chat_id = :id", {
                   'id': chat_id, 'status': status})


@connection_decorator
def get_annotations(chat_id, cursor=None):
    return cursor.execute("SELECT annotations FROM users WHERE chat_id = :id", {'id': chat_id}).fetchone()[0]


@connection_decorator
def set_last_request(chat_id, message_id, cursor=None):
    cursor.execute("UPDATE users SET last_serv_req = :last_serv_req WHERE chat_id = :chat_id", {
                   'chat_id': chat_id, 'last_serv_req': message_id})


@connection_decorator
def get_last_request(chat_id, cursor=None):
    return cursor.execute("SELECT last_serv_req FROM users WHERE chat_id = :id", {'id': chat_id}).fetchone()[0]
