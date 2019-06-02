import services

FULL_SERVICES = services.FULL_SERVICES
SERVICE_LINKS = services.SERVICE_LINKS

def is_it_link(text):
    for link in SERVICE_LINKS:
        if link in text:
            return True
    return False

def working_services(serv_codes):
    result = []
    if len(serv_codes) < len(FULL_SERVICES):
        while len(FULL_SERVICES) != len(serv_codes):
            serv_codes = '0' + serv_codes
    elif len(serv_codes) > len(FULL_SERVICES):
        serv_codes = '1' * len(FULL_SERVICES)
    for idx, i in enumerate(serv_codes):
        if int(i) == 1:
            result.append(FULL_SERVICES[idx])
    return result

def toggle_service(toggle, user_list):
    to_toggle = FULL_SERVICES.index(toggle)
    x = list(user_list)
    if user_list[to_toggle] == '0':
        x[to_toggle] = '1'
    else:
        x[to_toggle] = '0'
    return ''.join(x)

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

def send_from(message):
    if message.from_user.first_name != None and message.from_user.last_name:
        name = '{} {}'.format(message.from_user.first_name, message.from_user.last_name)
    elif message.from_user.username != None:
        name = '{}'.format(message.from_user.username)
    elif message.from_user.first_name != None:
        name = '{}'.format(message.from_user.first_name)
    else:
        name = '{GODS OF MUSIC}'
    return 'Sent by {}'.format(name)