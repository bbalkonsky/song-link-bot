from scripts.services import SERVICES


def is_it_link(text):
    for service in SERVICES:
        for link in SERVICES[service]['link']:
            if link in text:
                return True
    return False


def toggle_service(toggle, user_list):
    user_list[toggle] = 1 if user_list[toggle] == 0 else 0
    return user_list


def description_text(message):
    splitted = message.text.split('\n')

    if len(splitted) == 1:
        splitted = splitted[0].split(' ')
        link = splitted[-1]
        splitted.remove(link)
        res = ' '.join(splitted)
    else:
        last_split = splitted[-1].split(' ')
        link = last_split.pop(-1)
        splitted[-1] = splitted[-1].replace(link.strip(), '')
        res = '\n'.join(splitted)

    return res, link.strip()


def sent_from(message, link):
    if message.from_user.first_name != None and message.from_user.last_name:
        name = '{} {}'.format(message.from_user.first_name,
                              message.from_user.last_name)
    elif message.from_user.username != None:
        name = '{}'.format(message.from_user.username)
    elif message.from_user.first_name != None:
        name = '{}'.format(message.from_user.first_name)
    else:
        name = '{GODS OF MUSIC}'
    return 'Sent by[:]({}) {}'.format(link, name)
