from telebot import types
import telebot
import time
import configparser

from scripts.loging import log_write, error_write
from scripts.services import SERVICES, INSTRUCTIONS_RU, INSTRUCTIONS_EN
from scripts.helpers import is_it_link, toggle_service, description_text, send_from
from scripts.keyboards import create_keyboard
from scripts.linksearch import get_links, search_vk
from scripts.queries import first_connect, get_user_services, set_user_services, toggle_annotations, get_annotations, set_last_request, get_last_request, create_log_bases


config = configparser.ConfigParser()
config.read('config.ini')

base = config['FILES']['USER_BASE']
token = config['ACCESS']['TOKEN']

bot = telebot.TeleBot(token)


@bot.callback_query_handler(func=lambda callback: callback.data == 'done')
def handle_callback_done(callback_query):
    bot.delete_message(chat_id=callback_query.message.chat.id,
                       message_id=get_last_request(callback_query.message.chat.id))
    set_last_request(callback_query.message.chat.id, 0)
    bot.send_message(callback_query.message.chat.id,
                     text='Changes have been saved.')
    show_services(callback_query.message)


@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback_query):
    user_services_code = get_user_services(callback_query.message.chat.id)
    new_user_services_code = toggle_service(
        callback_query.data, user_services_code)
    set_user_services(callback_query.message.chat.id, new_user_services_code)
    edit_services(callback_query.message)


@bot.channel_post_handler(commands=['edit'])
@bot.message_handler(commands=['edit'])
def edit_services(message):
    user_services_code = get_user_services(message.chat.id)
    keyboard = create_keyboard(user_services_code)
    sended = bot.send_message(
        message.chat.id, text='Services:\n', reply_markup=keyboard)

    last_req = get_last_request(message.chat.id)
    sended

    if last_req == 0:
        set_last_request(sended.chat.id, sended.message_id)
    else:
        bot.delete_message(chat_id=message.chat.id, message_id=last_req)
        set_last_request(sended.chat.id, sended.message_id)


@bot.channel_post_handler(commands=['show'])
@bot.message_handler(commands=['show'])
def show_services(message):
    user_services = get_user_services(message.chat.id)
    returned = ''

    for serv in list(user_services.keys()):
        if user_services[serv]:
            returned += '\n{}'.format(SERVICES[serv]['alias'])
    bot.send_message(
        message.chat.id, text='*Your services:*\n {}'.format(returned), parse_mode='Markdown')


@bot.message_handler(commands=['start', 'info'])
def info(message):
    instructions = INSTRUCTIONS_RU if str(
        message.from_user.language_code) == 'ru' else INSTRUCTIONS_EN
    for i in instructions:
        bot.send_message(message.chat.id, text=i)
        time.sleep(1)


@bot.channel_post_handler(commands=['annotations'])
@bot.message_handler(commands=['annotations'])
def toggle(message):
    toggle_annotations(message.chat.id)
    annotations = get_annotations(message.chat.id)
    if annotations == 0:
        bot.send_message(message.chat.id, text='Annotations: off')
    else:
        bot.send_message(message.chat.id, text='Annotations: on')


@bot.channel_post_handler()
@bot.message_handler()
def handle_message(message):
    try:
        if is_it_link(message.text) is True:
            log_write(message)

            user_services = get_user_services(message.chat.id)
            annotations = get_annotations(message.chat.id)
            new_text, clear_link = description_text(message)
            if annotations == 0:
                new_text = ''

            links_list = get_links('{}'.format(clear_link), user_services)
            if len(links_list) > 0:
                links_to_send = str()
                for link in links_list:
                    link_title = '[{}]'.format(link[0])
                    link_link = '({})'.format(link[1])
                    links_to_send = links_to_send + \
                        '\n{}{}'.format(link_title, link_link)

                sender = str('')
                if message.chat.type == 'group':
                    sender = send_from(message)
                elif message.chat.type == 'channel':
                    sender = 'from @MuzShareBot'

                bot.send_message(message.chat.id,
                                 text='{}\n{}\n\n{}\n\n'.format(
                                     new_text, links_to_send, sender),
                                 parse_mode='Markdown')

                bot.delete_message(chat_id=message.chat.id,
                                   message_id=message.message_id)
            else:
                bot.send_message(
                    message.chat.id, text="I couldn't find this one =(")

    except Exception as ex:
        print('HUI')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        error = template.format(type(ex).__name__, ex.args)
        error_write(message, error)


def main():
    first_connect()
    create_log_bases()
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
