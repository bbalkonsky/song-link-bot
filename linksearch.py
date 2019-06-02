import requests
from bs4 import BeautifulSoup

def get_links(message, user_on):
    headers = {'User-Agent': 'My User Agent 1.0'}
    adress = 'https://song.link/{}'.format(message)
    response = requests.get(adress, headers=headers)

    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, 'lxml')
    links_holder = soup.find('div', text='LISTEN').parent
    all_links = links_holder.find_all('a')
    
    result_list = []
    
    for link in all_links:
      link_title = link['data-test'].split(':')[1]
      if link_title in user_on:
        result_list.append((link_title, link['href']))
    
    if 'vkontakte' in user_on:
      vk_link = search_vk(response)
      result_list.append(vk_link)
    return result_list

def search_vk(request):
    soup = BeautifulSoup(request.text, 'lxml')
    artist = soup.find("button").parent.previous
    name = artist.previous.previous

    song_name = ' '.join([artist, name])
    song = song_name.replace(' ', '%20').replace('(', '%28').replace(')', '%29')
    
    return ('vkontakte', 'https://vk.com/search?c%5Bper_page%5D=200&c%5Bq%5D={}&c%5Bsection%5D=audio'.format(song))