import requests
import json
from scripts.services import SERVICES


def get_links(message, user_on):
    params = (
        ('url', message),
        ('key', '788c8d13-5d08-464d-838f-5825ce494d29'),
    )
    response = requests.get(
        'https://api.song.link/v1-alpha.1/links', params=params)
    result_list = []

    if response.status_code == 200:
        links_list = json.loads(response.text)

        for service in list(user_on.keys()):
            if user_on[service]:
                if service in links_list['linksByPlatform']:
                    service_name = SERVICES[service]['alias']
                    service_link = links_list['linksByPlatform'][service]['url'] if service != 'tidal' else links_list['linksByPlatform'][service]['url'].replace(
                        'listen.', '')
                    result_list.append((service_name, service_link))

        if user_on['vk']:
            for i in links_list['entitiesByUniqueId'].values():
                if i['apiProvider'] == 'youtube':
                    continue
                song_name = ' '.join([i['artistName'], i['title']])
                break
            result_list.append(search_vk(song_name))

        return result_list


def search_vk(song_name):
    song_name = song_name.replace(' ', '%20').replace(
        '(', '%28').replace(')', '%29')
    return (SERVICES['vk']['alias'], 'https://vk.com/search?c%5Bper_page%5D=200&c%5Bq%5D={}&c%5Bsection%5D=audio'.format(song_name))
