from scripts.services import SERVICES
from telebot import types
import collections


def create_keyboard(user_services):
    sorted_services = collections.OrderedDict(sorted(user_services.items()))
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    for key in sorted(list(sorted_services.keys())):
        if sorted_services[key]:
            buttons.append(types.InlineKeyboardButton(text='-{}'.format(SERVICES[key]['alias']),
                                                      callback_data='{}'.format(SERVICES[key]['name']))
                           )
        else:
            buttons.append(types.InlineKeyboardButton(text='+{}'.format(SERVICES[key]['alias']),
                                                      callback_data='{}'.format(SERVICES[key]['name']))
                           )
    buttons.append(types.InlineKeyboardButton(
        text='Done', callback_data='done'))

    keyboard.add(*buttons)
    return keyboard


def create_links_keyboard(links):
    sorted_links = sorted(links, key=lambda x: x[0])
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    for link in sorted_links:
        buttons.append(types.InlineKeyboardButton(text=link[0], url=link[1]))
    keyboard.add(*buttons)
    return keyboard
