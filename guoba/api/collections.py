from flask import Blueprint, jsonify, abort, request
from guoba.models import Collection
from guoba import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

collections = Blueprint('collections', __name__, url_prefix='/collections')


def verify_password(password_hash, password):
    if password_hash is None:
        return True
    if password is None:
        return False
    return check_password_hash(password_hash, password)


def get_password_hash(password, default=None):
    return generate_password_hash(password) if password is not None else default


@collections.route('/<uuid:collection_id>', methods=['GET'])
def get_collection(collection_id):
    db_collection = Collection.query.filter_by(id=collection_id).first_or_404()
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
    db.session.commit()

    return jsonify(collection.serialize)


@collections.route('/<uuid:collection_id>', methods=['PUT'])
def put_collection(collection_id):
    db_collection = Collection.query.filter_by(id=collection_id).first_or_404()

    data = request.values
    if not verify_password(db_collection.password_hash, data.get('password')):
        abort(401)

    collection = Collection(
        id=db_collection.id,
        name=data.get('name'),
        data=data.get('data'),
        password_hash=get_password_hash(data.get('set_password')),
    )

    db.session.delete(db_collection)
    db.session.flush()
    db.session.add(collection)
    db.session.commit()

    return jsonify(collection.serialize)


@collections.route('/<uuid:collection_id>', methods=['PATCH'])
def patch_collection(collection_id):
    db_collection = Collection.query.filter_by(id=collection_id).first_or_404()

    data = request.values
    if not verify_password(db_collection.password_hash, data.get('password')):
        abort(401)

    db_collection.name = data.get('name', db_collection.name)
    db_collection.data = data.get('data')   # todo implement partial patch
    db_collection.password_hash = get_password_hash(data.get('set_password'), db_collection.password_hash)
    db_collection.date_modified = datetime.utcnow()

    return jsonify(db_collection.serialize)
