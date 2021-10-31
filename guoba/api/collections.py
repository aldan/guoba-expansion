from flask import Blueprint, jsonify, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
from guoba.models import Collection, Character, Weapon
from guoba import db
from copy import deepcopy
from datetime import datetime
from json import load, loads, dumps
from jsonschema import validate, ValidationError
import os
from config import JSON_SCHEMA_DIR
from functools import wraps
from sqlalchemy.orm.attributes import flag_modified

collections = Blueprint('collections', __name__, url_prefix='/collections')
with open(os.path.join(JSON_SCHEMA_DIR, 'collection.data.json'), 'r') as schema:
    collection_data_schema = load(schema)


def verify_password(password_hash, password):
    if password_hash is None:
        return True
    if password is None:
        return False
    return check_password_hash(password_hash, password)


def get_password_hash(password, default=None):
    return generate_password_hash(password) if password is not None else default


def validate_json(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        new_args = []
        to_validate = kwargs.get('to_validate', ())
        for i in range(len(args)):
            arg = args[i]
            try:
                if isinstance(arg, str):
                    arg = loads(arg)
                assert isinstance(arg, dict)
            except (ValueError, AssertionError):
                abort(422, description='collection.data: invalid JSON syntax')
            if i in to_validate:
                try:
                    validate(arg, collection_data_schema)
                except ValidationError:
                    abort(422, description='collection.data: invalid JSON schema')
            new_args.append(arg)
        args = tuple(new_args)
        return func(*args, **kwargs)
    return wrapped_func


def merge(target, patch):
    if patch is None:
        return
    for key, value in patch.items():
        if isinstance(value, dict) and key in target and isinstance(target[key], dict):
            merge(target[key], value)
        else:
            target[key] = value


@validate_json
def update_collection_data(data, patch=None, to_validate=None):
    merge(data, patch)
    if len(data['users']) > 10:
        abort(422, description='collection.data: too many users')

    # update character data
    characters_list = [character[0] for character in db.session.query(Character.id).all()]
    characters_dict = deepcopy(data['characters'])
    data['characters'] = {}
    for character_id in characters_list:
        character_ownership = {}
        for user_id in data['users']:
            try:
                character_ownership[user_id] = int(characters_dict[character_id][user_id])
            except (KeyError, ValueError):
                character_ownership[user_id] = -1
        data['characters'][character_id] = character_ownership

    # update weapon data
    weapons_list = [weapon[0] for weapon in db.session.query(Weapon.id).all()]
    weapons_dict = deepcopy(data['weapons'])
    data['weapons'] = {}
    for weapon_id in weapons_list:
        weapon_ownership = {}
        for user_id in data['users']:
            try:
                weapon_ownership[user_id] = int(weapons_dict[weapon_id][user_id])
            except (KeyError, ValueError):
                weapon_ownership[user_id] = -1
        data['weapons'][weapon_id] = weapon_ownership

    return data


@collections.route('/<uuid:collection_id>', methods=['GET'])
def get_collection(collection_id):
    db_collection = Collection.query.filter_by(id=collection_id).first_or_404(description='Resource not found')
    return jsonify(db_collection.serialize)


@collections.route('/', methods=['POST'], strict_slashes=False)
def post_collection():
    data = request.values
    post_data = update_collection_data(data.get('data'), to_validate=(0,)) if data.get('data') else None
    collection = Collection(
        name=data.get('name'),
        data=post_data,
        password_hash=get_password_hash(data.get('set_password')),
    )
    db.session.add(collection)
    db.session.commit()

    return jsonify(collection.serialize)


@collections.route('/<uuid:collection_id>', methods=['PUT'])
def put_collection(collection_id):
    db_collection = Collection.query.filter_by(id=collection_id).first_or_404(description='Resource not found')
    data = request.values
    if not verify_password(db_collection.password_hash, data.get('password')):
        abort(401, description='Wrong password supplied')

    post_data = update_collection_data(data.get('data'), to_validate=(0,)) if data.get('data') else None
    collection = Collection(
        id=db_collection.id,
        name=data.get('name'),
        data=post_data,
        password_hash=get_password_hash(data.get('set_password')),
    )
    db.session.delete(db_collection)
    db.session.flush()
    db.session.add(collection)
    db.session.commit()

    return jsonify(collection.serialize)


@collections.route('/<uuid:collection_id>', methods=['PATCH'])
def patch_collection(collection_id):
    db_collection = Collection.query.filter_by(id=collection_id).first_or_404(description='Resource not found')
    data = request.values
    if not verify_password(db_collection.password_hash, data.get('password')):
        abort(401, description='Wrong password supplied')

    db_collection.name = data.get('name', db_collection.name)
    if data.get('data'):
        db_collection.data = update_collection_data(db_collection.data, data.get('data'), to_validate=(1,))
        flag_modified(db_collection, 'data')
    db_collection.password_hash = get_password_hash(data.get('set_password'), db_collection.password_hash)
    db_collection.date_modified = datetime.utcnow()
    db.session.commit()

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
