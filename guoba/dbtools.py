import click
from flask import Blueprint
import ghhw
from guoba.models import db, Character, Weapon, Collection
from datetime import datetime

dbtools = Blueprint('dbtools', __name__)


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
    print(f'{len(characters)} character record(s) to be synchronized')


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
    print(f'{len(weapons)} weapon record(s) to be synchronized')


@dbtools.cli.command('sync')
@click.argument('resource', required=False)
def sync(resource):
    """Synchronizes specified database resource

    Arguments:
    resource -- resource type [character, weapon], if none is specified all resources are synchronized
    """
    if resource is None:
        update_characters()
        update_weapons()

    if resource == 'character':
        update_characters()

    if resource == 'weapon':
        update_weapons()

    db.session.commit()
    print('Finished')


@dbtools.cli.command('delete')
@click.argument('resource_type')
@click.argument('resource', required=False)
def delete(resource_type, resource):
    """Deletes resource with specified ID

    Arguments:
    resource_type -- resource type [collection]
    resource      -- ID of resource, if none is specified all resources of the type are deleted
    """

    if resource_type == 'collection':
        if resource:
            query = Collection.query.filter_by(id=resource)
            if query.first():
                query.delete()
                print(f'{query.first()} to be deleted')
        else:
            count = Collection.query.count()
            Collection.query.delete()
            print(f'{count} record(s) to be deleted')

    db.session.commit()
    print('Finished')
