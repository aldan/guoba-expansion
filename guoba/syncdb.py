from flask import Blueprint
from guoba import db
import ghhw
from guoba.models import Character, Weapon
from datetime import datetime

syncdb = Blueprint('syncdb', __name__)


def update_characters():
    characters = ghhw.get_characters()

    for character in characters:
        media = ghhw.get_character_media(character['id'])
        db_character = Character(
            id=character['id'],
            name=character['name'],
            date_synced=datetime.utcnow(),
            rarity=int(character['rarity']),
            element=character['element'],
            weapon_type=character['weapon'],
            img_card=media['img_card'],
            img_icon=media['img_icon'],
            img_gacha_card=media['img_gacha_card'],
            img_gacha_splash=media['img_gacha_splash'],
        )
        db.session.merge(db_character)


def update_weapons():
    weapons = ghhw.get_weapons()

    for weapon in weapons:
        media = ghhw.get_weapon_media(weapon['id'])
        db_weapon = Weapon(
            id=weapon['id'],
            name=weapon['name'],
            date_synced=datetime.utcnow(),
            rarity=int(weapon['rarity']),
            img_icon=media['img_icon'],
            img_icon_ascended=media['img_icon_ascended'],
            img_gacha_card=media['img_gacha_card'],
        )
        db.session.merge(db_weapon)


@syncdb.cli.command('all')
def syncdb_all():
    """ Synchronizes all items in database """
    update_characters()
    update_weapons()
    db.session.commit()
