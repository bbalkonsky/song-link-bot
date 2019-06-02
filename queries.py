import sqlite3
import configparser
import services

config = configparser.ConfigParser()
config.read('config.ini')

FULL_SERVICES = services.FULL_SERVICES
base = config['FILES']['BASE_FILE']


def connection(fn):
    def wrapped(*args):
        connection = sqlite3.connect(base)
        cursor = connection.cursor()
        query = fn(*args, cursor)
        connection.commit()
        connection.close()
        return(query)
    return wrapped

@connection
def first_connect(cursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS users(chat_id text, services text, last_serv_req, annotations)')

@connection
def toggle_annotations(chat_id, cursor):
    status = cursor.execute("SELECT annotations FROM users WHERE chat_id = :id", {'id': chat_id}).fetchone()[0]
    if status == 1:
        status = 0
    else:
        status = 1
    cursor.execute("UPDATE users SET annotations = :status WHERE chat_id = :id", {'id': chat_id, 'status': status})

@connection
def get_annotations(chat_id, cursor): 
    return cursor.execute("SELECT annotations FROM users WHERE chat_id = :id", {'id': chat_id}).fetchone()[0]

@connection
def get_user_services(id, cursor):
    services_value = len(FULL_SERVICES)    
    query = cursor.execute("SELECT services FROM users WHERE chat_id = :id", {'id': id}).fetchone()
    if query != None:
        return query[0]
    else:
        cursor.execute("INSERT INTO users VALUES (:chat_id, :services, :last_serv_req, :annotations)", 
                       {'chat_id': id, 'services': '1'*services_value, 'last_serv_req': 0, 'annotations': 0})
        return '1'*services_value

@connection
def set_user_services(id, codes, cursor):
    cursor.execute("UPDATE users SET services = :services WHERE chat_id = :chat_id", {'chat_id': id, 'services': codes})
    
@connection
def set_last_request(chat_id, message_id, cursor):
    cursor.execute("UPDATE users SET last_serv_req = :last_serv_req WHERE chat_id = :chat_id", {'chat_id': chat_id, 'last_serv_req': message_id})

@connection
def get_last_request(chat_id, cursor):
    return cursor.execute("SELECT last_serv_req FROM users WHERE chat_id = :id", {'id': chat_id}).fetchone()[0]