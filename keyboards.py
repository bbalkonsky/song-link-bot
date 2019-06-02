import services
from telebot import types

FULL_SERVICES = services.FULL_SERVICES
STAT_TYPES = services.STAT_TYPES

def create_keyboard(user_services_code):
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    for idx, i in enumerate(user_services_code):
        if i == '1':
            buttons.append(types.InlineKeyboardButton(text='-{}'.format(FULL_SERVICES[idx]), callback_data='{}'.format(FULL_SERVICES[idx])))
        elif i == '0':
            buttons.append(types.InlineKeyboardButton(text='+{}'.format(FULL_SERVICES[idx]), callback_data='{}'.format(FULL_SERVICES[idx])))
    buttons.append(types.InlineKeyboardButton(text='Done', callback_data='done')) 
    
    keyboard.add(*buttons)
    return keyboard

def stat_keyboard(fullness=False):
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    if fullness == False:
        for idx, i in enumerate(STAT_TYPES):
            if idx < 4:
                buttons.append(types.InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))
                
        buttons.append(types.InlineKeyboardButton(text='Show more', callback_data='more_stat'))
        keyboard.add(*buttons)
        return keyboard
    else:
        for i in STAT_TYPES:
            buttons.append(types.InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))
        keyboard.add(*buttons)
        return keyboard