from ghhw import conf
import requests
from bs4 import BeautifulSoup as bs


uri_characters = {
    'live': r'/db/char/characters/',
    'beta': r'/db/char/unreleased-and-upcoming-characters/',
    'base': r'/db/char/',
    'img':  r'/img/char/',
}

elements = ['pyro', 'hydro', 'electro', 'cryo', 'anemo', 'geo', 'dendro']
weapons = ['sword', 'claymore', 'polearm', 'bow', 'catalyst']


def get_characters(release=None, **kwargs):
    if release is None:
        release = 'live'

    characters_uri = uri_characters[release]
    res = requests.get(conf.generate_url(characters_uri))
    content = res.content
    soup = bs(content, 'html.parser')

    character_list = []
    character_filter = {}
    for arg, val in kwargs.items():
        character_filter[arg] = val

    char_containers = soup.find_all('div', {'class': 'char_sea_cont'})
    for container in char_containers:
        links = container.find_all('a')
        ref, title = links[:2]
        stars_container = container.find('div', {'class': 'sea_charstarcont'})
        weapon_link = container.find('img', {'class': 'sea_weptype_element'})['data-src']

        url = title['href']
        char_id = url.split('/')[3]
        name = title.span.text
        rarity = str(len(stars_container.find_all('svg')))
        element = next((elem for elem in elements if elem in ref.find_all('img')[1]['data-src']), None)
        weapon = next((weap for weap in weapons if weap in weapon_link), None)
        character = {
            'id': char_id,
            'url': url,
            'name': name,
            'rarity': rarity,
            'element': element,
            'weapon': weapon,
        }
        if all(character[arg] == character_filter[arg] for arg in kwargs.keys()):
            character_list.append(character)

    return character_list


def get_character_media(character_id):

    img_card = conf.generate_url(f'{uri_characters["img"]}{character_id}.png/')
    img_icon = conf.generate_url(f'{uri_characters["img"]}{character_id}_face.png/')
    img_gacha_card = conf.generate_url(f'{uri_characters["img"]}{character_id}_gacha_card.png/')
    img_gacha_splash = conf.generate_url(f'{uri_characters["img"]}{character_id}_gacha_splash.png/')

    character_media = {
        'id': character_id,
        'img_card': img_card,
        'img_icon': img_icon,
        'img_gacha_card': img_gacha_card,
        'img_gacha_splash': img_gacha_splash,
    }

    return character_media
