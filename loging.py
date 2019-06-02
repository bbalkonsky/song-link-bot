import configparser
import datetime
import time

config = configparser.ConfigParser()
config.read('config.ini')

log_file = config['FILES']['LOG_FILE']
error_log_file = config['FILES']['ERROR_LOG_FILE']

def log(message):
    if message.chat.type != 'channel':
        if str(message.from_user.id) == '126017510':
            return

    text = message.text.replace('\n', ' ').strip().split(' ')[-1]
    
    service = ''
    
    # TODO вот тут 
    serv = ['music.apple', 'spotify', 'youtube', 'deezer', 'google', 'soundcloud', 'yandex', 'tidal', 'napster', 'pandora.com']
    for i in serv:
        if i in text:
            service = i
            break
        
    time = datetime.datetime.fromtimestamp(message.date).strftime("%d.%m.%Y %H:%M")
    if message.chat.type == 'channel':
        to_log = ('{} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {}\n'.format(message.chat.type, message.chat.id, message.chat.username, message.chat.title, message.author_signature, 'None', 'None', 'None', time, service, text))
    elif message.chat.type == 'group':
        to_log = ('{} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {}\n'.format(message.chat.type, message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, message.chat.id, message.chat.title, message.from_user.language_code, time, service, text))
    elif message.chat.type == 'private':
        to_log = ('{} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {}\n'.format(message.chat.type, message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, 'None', 'None', message.from_user.language_code, time, service, text))

    with open(log_file, 'a') as f:
        f.write(to_log)

def error_log(message, error):
    to_log = 'Message:\n{}\n\nError:\n{}\n\n\n'.format(message, error)
    with open(error_log_file, 'a') as f:
        f.write(to_log)