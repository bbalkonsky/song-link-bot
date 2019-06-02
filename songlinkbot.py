import configparser
import json
import os
import time

import telebot

from loging import log, error_log
from linksearch import get_links
from helpers import is_it_link, working_services, toggle_service, description_text, send_from
import services
from statistic import get_stat, send_stat
from keyboards import  create_keyboard, stat_keyboard
from queries import first_connect, toggle_annotations, get_annotations, get_user_services, get_last_request, set_user_services, set_last_request

config = configparser.ConfigParser()
config.read('config.ini')

ALIASES = services.ALIASES
STAT_TYPES = services.STAT_TYPES

token = config['ACCESS']['TOKEN']

bot = telebot.TeleBot(token)

@bot.callback_query_handler(func=lambda callback: callback.data in STAT_TYPES)
def handle_callback(callback_query):
    stats = callback_query.data.split(' ')
    period = stats[0]
    statistic = stats[1]
    response = send_stat(period, statistic)
    if type(response) is not str:
        bot.send_photo(126017510, open('daily_queries.png', 'rb'))
        os.remove('daily_queries.png')
    else:
        bot.send_message(126017510, text=response)

@bot.callback_query_handler(func=lambda callback: callback.data == 'more_stat')
def handle_callback(callback_query):
    keyboard = stat_keyboard(True)
    bot.send_message(callback_query.from_user.id, text = 'Which one?', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda callback: callback.data == 'done')
def handle_callback(callback_query):
    bot.delete_message(chat_id=callback_query.message.chat.id, message_id=get_last_request(callback_query.message.chat.id))
    set_last_request(callback_query.message.chat.id, 0)
    bot.send_message(callback_query.message.chat.id, text='Changes have been saved.')
    show_services(callback_query.message)
        
@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback_query):
    user_services_code = get_user_services(callback_query.message.chat.id)
    new_user_services_code = toggle_service(callback_query.data, user_services_code)
    set_user_services(callback_query.message.chat.id, new_user_services_code)
    edit_services(callback_query.message)

@bot.message_handler(commands=['stat'])
def stat(message):
    keyboard = stat_keyboard()
    bot.send_message(message.chat.id, text = 'Which one?', reply_markup=keyboard)

@bot.channel_post_handler(commands=['toggle'])
@bot.message_handler(commands=['toggle_annotations', 'toggle'])
def toggle(message):       
    toggle_annotations(message.chat.id)
    annotations = get_annotations(message.chat.id)
    if annotations == 0:
        bot.send_message(message.chat.id, text = 'Annotations: off')
    else:
        bot.send_message(message.chat.id, text = 'Annotations: on')
            
@bot.channel_post_handler(commands=['edit'])
@bot.message_handler(commands=['edit_services', 'edit'])
def edit_services(message):
    user_services_code = get_user_services(message.chat.id)
    keyboard = create_keyboard(user_services_code) 
    sended = bot.send_message(message.chat.id, text = 'Services:\n', reply_markup=keyboard)
    
    last_req = get_last_request(message.chat.id)
    sended

    if last_req == 0:
      set_last_request(sended.chat.id, sended.message_id)
    else:
      bot.delete_message(chat_id=message.chat.id, message_id=last_req) 
      set_last_request(sended.chat.id, sended.message_id)
    
@bot.channel_post_handler(commands=['show'])
@bot.message_handler(commands=['show_services', 'show'])
def show_services(message):
    user_services_code = get_user_services(message.chat.id)
    user_services = working_services(user_services_code)
    returned = ''
    
    for serv in user_services:
        if serv in ALIASES:
            returned += '\n{}'.format(ALIASES[serv])
        else:
            returned += '\n{}'.format(serv.title())
    bot.send_message(message.chat.id, text = '*Your services:*\n {}'.format(returned), parse_mode='Markdown')
    
@bot.message_handler(commands=['start', 'info'])
def info(message):
    instructions = services.INSTRUCTIONS_RU if str(message.from_user.language_code) == 'ru' else services.INSTRUCTIONS_EN
    for i in instructions:
        bot.send_message(message.chat.id, text = i) 
        time.sleep(1)

@bot.channel_post_handler()
@bot.message_handler()
def handle_message(message):
    try:
        if is_it_link(message.text) is True:
            log(message)
            
            user_services_code = get_user_services(message.chat.id)
            user_services = working_services(user_services_code)
            annotations = get_annotations(message.chat.id)
            new_text, clear_link = description_text(message)
            if annotations == 0:
                new_text = ''

            links_list = get_links('{}'.format(clear_link), user_services)
            if len(links_list) > 0:
                links_to_send = str()
                for link in links_list:
                    if link[0] == 'tidal': 
                        link = (link[0], link[1].replace('listen.', ''))
                        link_title = '[{}]'.format(link[0].title())
                    elif link[0] in ALIASES:
                        link_title = '[{}]'.format(ALIASES[link[0]])
                    else:
                        link_title = '[{}]'.format(link[0].title())
                    link_link = '({})'.format(link[1])
                    links_to_send = links_to_send + '\n{}{}'.format(link_title, link_link)
  
                sender = str('')
                if message.chat.type == 'group':
                    sender = send_from(message)
                elif message.chat.type == 'channel':
                    sender = 'from @MuzShareBot'
                  
                bot.send_message(message.chat.id,
                                text='{}\n{}\n\n{}\n\n'.format(new_text, links_to_send, sender), 
                                parse_mode='Markdown')
                
                try: bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                except Exception as ex:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    error = template.format(type(ex).__name__, ex.args)
                    error_log(message, error)
            else: 
                bot.send_message(message.chat.id, text="I couldn't find this one =(")
                
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        error = template.format(type(ex).__name__, ex.args)
        error_log(message, error)

def main():        
    first_connect()
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()