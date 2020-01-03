import requests
import json
from scripts.services import SERVICES
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

api_token = config['ACCESS']['API_TOKEN']

def get_api_request(message):
    params = (
        ('url', message),
        ('key', api_token),
    )
    return requests.get(
        'https://api.song.link/v1-alpha.1/links', params=params)


def get_links(response, user_on):
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


def get_song_name(response):
    song = json.loads(response.text)
    for i in song['entitiesByUniqueId'].values():
        return '{} - {}'.format(i['artistName'], i['title'])
