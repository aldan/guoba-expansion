from flask import Blueprint, jsonify, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
from guoba.models import Collection, Character, Weapon
from guoba import db
from copy import deepcopy
from datetime import datetime
from json import loads

collections = Blueprint('collections', __name__, url_prefix='/collections')


def verify_password(password_hash, password):
    if password_hash is None:
        return True
    if password is None:
        return False
    return check_password_hash(password_hash, password)


def get_password_hash(password, default=None):
    return generate_password_hash(password) if password is not None else default


def update_collection_data(data, patch=None):
    new_data = {
        'users': {},
        'characters': {},
        'weapons': {},
    }

    try:
        if isinstance(data, str):
            data = loads(data)
        if patch:
            patch = loads(patch)
        else:
            patch = deepcopy(new_data)
    except ValueError:
        abort(422, description='collection.data: invalid JSON syntax')

    try:
        # update user data
        default_ownership = {}
        for user_id, user_data in data['users'].items():
            if not user_id.isdigit():
                continue
            new_data['users'][user_id] = {
                'name': user_data['name'],
            }
            default_ownership[user_id] = -1

        try:
            for user_id, user_data in patch['users'].items():
                if not user_id.isdigit():
                    continue
                new_data['users'][user_id] = {
                    'name': user_data['name'],
                }
                default_ownership[user_id] = -1
        except (KeyError, ValueError):
            pass

        if not (1 <= len(new_data['users']) <= 10):
            abort(422, description='collection.data: number of users must be in range [1-10]')

        # update character data
        characters_list = [character[0] for character in db.session.query(Character.id).all()]
        for character_id in characters_list:
            character_ownership = deepcopy(default_ownership)
            for user_id in character_ownership:
                try:
                    character_ownership[user_id] = int(data['characters'][character_id][user_id])
                    assert -1 <= character_ownership[user_id] <= 6
                except (KeyError, ValueError, AssertionError):
                    character_ownership[user_id] = -1
                try:
                    character_ownership[user_id] = int(patch['characters'][character_id][user_id])
                    assert -1 <= character_ownership[user_id] <= 6
                except (KeyError, ValueError, AssertionError):
                    character_ownership[user_id] = -1

            new_data['characters'][character_id] = character_ownership

        # update weapon data
        weapons_list = [weapon[0] for weapon in db.session.query(Weapon.id).all()]
        for weapon_id in weapons_list:
            weapon_ownership = deepcopy(default_ownership)
            for user_id in weapon_ownership:
                try:
                    weapon_ownership[user_id] = int(data['weapons'][weapon_id][user_id])
                    assert -1 <= weapon_ownership[user_id] <= 6
                except (KeyError, ValueError, AssertionError):
                    weapon_ownership[user_id] = -1
                try:
                    weapon_ownership[user_id] = int(patch['weapons'][weapon_id][user_id])
                    assert -1 <= weapon_ownership[user_id] <= 6
                except (KeyError, ValueError, AssertionError):
                    weapon_ownership[user_id] = -1

            new_data['weapons'][weapon_id] = weapon_ownership
        return new_data
    except (KeyError, ValueError):
        abort(422, description='collection.data: JSON data is corrupted')


@collections.route('/<uuid:collection_id>', methods=['GET'])
def get_collection(collection_id):
    db_collection = Collection.query.filter_by(id=collection_id).first_or_404(description='Resource not found')
    return jsonify(db_collection.serialize)


@collections.route('/', methods=['POST'], strict_slashes=False)
def post_collection():
    data = request.values
    collection = Collection(
        name=data.get('name'),
        data=data.get('data'),
        password_hash=get_password_hash(data.get('set_password')),
    )

    db.session.add(collection)
    db.session.flush()
    collection.data = update_collection_data(collection.data)
    db.session.commit()

    return jsonify(collection.serialize)


@collections.route('/<uuid:collection_id>', methods=['PUT'])
def put_collection(collection_id):
    db_collection = Collection.query.filter_by(id=collection_id).first_or_404(description='Resource not found')

    data = request.values
    if not verify_password(db_collection.password_hash, data.get('password')):
        abort(401, description='Wrong password supplied')

    collection = Collection(
        id=db_collection.id,
        name=data.get('name'),
        data=data.get('data'),
        password_hash=get_password_hash(data.get('set_password')),
    )

    db.session.delete(db_collection)
    db.session.flush()
    db.session.add(collection)
    db.session.flush()
    collection.data = update_collection_data(collection.data)
    db.session.commit()

    return jsonify(collection.serialize)


@collections.route('/<uuid:collection_id>', methods=['PATCH'])
def patch_collection(collection_id):
    db_collection = Collection.query.filter_by(id=collection_id).first_or_404(description='Resource not found')

    data = request.values
    if not verify_password(db_collection.password_hash, data.get('password')):
        abort(401, description='Wrong password supplied')

    db_collection.name = data.get('name', db_collection.name)
    db_collection.data = update_collection_data(db_collection.data, data.get('data'))
    db_collection.password_hash = get_password_hash(data.get('set_password'), db_collection.password_hash)
    db_collection.date_modified = datetime.utcnow()

    return jsonify(db_collection.serialize)


@collections.route('/<uuid:collection_id>', methods=['DELETE'])
def delete_collection(collection_id):
    db_collection = Collection.query.filter_by(id=collection_id).first_or_404(description='Resource not found')

    data = request.values
    if not verify_password(db_collection.password_hash, data.get('password')):
        abort(401, description='Wrong password supplied')

    db.session.delete(db_collection)
    db.session.commit()

    return jsonify({
        'success': True,
        'error': None,
    })
