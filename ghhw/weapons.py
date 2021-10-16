from ghhw import conf
import requests
from bs4 import BeautifulSoup as bs


uri_weapons = {
    'base': r'/db/weapon/',
    'img':  r'/img/weapon/',
}

weapon_types = ['sword', 'claymore', 'polearm', 'bow', 'catalyst']


def get_weapons(wtypes=None, **kwargs):
    if wtypes is None:
        wtypes = weapon_types
    if not isinstance(wtypes, list):
        raise ValueError('wtypes is not a list')
    if any(wtype not in weapon_types for wtype in wtypes):
        raise ValueError('invalid weapon type')

    weapon_list = []
    for wtype in wtypes:
        weapon_list += get_weapons_by_type(wtype, **kwargs)

    return weapon_list


def get_weapons_by_type(wtype, **kwargs):
    res = requests.get(conf.generate_url(f'{uri_weapons["base"]}{wtype}/'))
    content = res.content
    soup = bs(content, 'html.parser')

    weapon_list = []
    weapon_filter = {}
    for arg, val in kwargs.items():
        weapon_filter[arg] = val

    weapon_table = soup.find('table', {'class': 'art_stat_table'})
    weapon_rows = weapon_table.find_all('tr')[1:]  # remove header row

    for row in weapon_rows:
        columns = row.find_all('td')[2:]  # first column is empty & 2nd is an icon

        url = columns[0].a['href']
        weapon_id = url.split('/')[3]
        name = columns[0].a.text
        rarity = str(len(columns[1].find_all('svg')))
        atk = columns[2].text
        substat = columns[3].text
        substat_val = columns[4].text
        special_ability = columns[5].text
        weapon = {
            'id': weapon_id,
            'url': url,
            'name': name,
            'rarity': rarity,
            'atk': atk,
            'substat': substat,
            'substat_val': substat_val,
            'special_ability': special_ability,
        }
        if all(weapon[arg] == weapon_filter[arg] for arg in kwargs.keys()):
            weapon_list.append(weapon)

    return weapon_list


def get_weapon_media(weapon_id):
    img_icon = conf.generate_url(f'{uri_weapons["img"]}{weapon_id}.png/')
    img_icon_ascended = conf.generate_url(f'{uri_weapons["img"]}{weapon_id}_a.png/')
    img_gacha_card = conf.generate_url(f'{uri_weapons["img"]}{weapon_id}_gacha.png/')

    weapon_media = {
        'id': weapon_id,
        'img_icon': img_icon,
        'img_icon_ascended': img_icon_ascended,
        'img_gacha_card': img_gacha_card,
    }

    return weapon_media
