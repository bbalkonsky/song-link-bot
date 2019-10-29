from scripts.services import SERVICES
from telebot import types


def create_keyboard(user_services):
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    for key in sorted(list(user_services.keys())):
        if user_services[key]:
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
