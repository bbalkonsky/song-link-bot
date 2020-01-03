import telebot
import configparser

from scripts.loging import *
from scripts.services import *
from scripts.helpers import *
from scripts.keyboards import *
from scripts.linksearch import *
from scripts.queries import *


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

            api_response = get_api_request('{}'.format(clear_link))
            links_list = get_links(api_response, user_services)

            if len(links_list) > 0:
                links_keyboard = create_links_keyboard(links_list)

                if message.chat.type == 'group' or message.chat.type == 'supergroup':
                    description = sent_from(message, clear_link)
                elif message.chat.type == 'channel':
                    description = '[from]({})  @muzShareBot'.format(clear_link)
                else:
                    description = '[{}]({})'.format(u'\U0001F3A7', message.text)

                bot.send_message(message.chat.id, text='{}\n\n{}'.format(new_text, description), parse_mode='Markdown',
                                 reply_markup=links_keyboard)
                bot.delete_message(chat_id=message.chat.id,
                                   message_id=message.message_id)

            else:
                bot.send_message(
                    message.chat.id, text="I couldn't find this one =(")

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        error = template.format(type(ex).__name__, ex.args)
        error_write(message, error)


def main():
    first_connect()
    create_log_bases()
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
