# guoba/models.py

from guoba import db
from sqlalchemy.dialects.postgresql import UUID, JSON
from werkzeug.security import generate_password_hash
import uuid
from datetime import datetime


class Item(db.Model):
    __abstract__ = True
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128))
    date_synced = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)


class Character(Item):
    __tablename__ = 'characters'
    rarity = db.Column(db.Integer, nullable=False)
    element = db.Column(db.String(16), nullable=False)
    weapon_type = db.Column(db.String(16), nullable=False)
    img_card = db.Column(db.Text)
    img_icon = db.Column(db.Text)
    img_gacha_card = db.Column(db.Text)
    img_gacha_splash = db.Column(db.Text)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_synced': self.date_synced.timestamp(),
            'rarity': self.rarity,
            'element': self.element,
            'weapon_type': self.weapon_type,
            'img_card': self.img_card,
            'img_icon': self.img_icon,
            'img_gacha_card': self.img_gacha_card,
            'img_gacha_splash': self.img_gacha_splash,
        }

    def __repr__(self):
        return f'<character:{self.id}>'


class Weapon(Item):
    __tablename__ = 'weapons'
    rarity = db.Column(db.Integer, nullable=False)
    img_icon = db.Column(db.Text)
    img_icon_ascended = db.Column(db.Text)
    img_gacha_card = db.Column(db.Text)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_synced': self.date_synced.timestamp(),
            'rarity': self.rarity,
            'img_icon': self.img_icon,
            'img_icon_ascended': self.img_icon_ascended,
            'img_gacha_card': self.img_gacha_card,
        }

    def __repr__(self):
        return f'<weapon:{self.id}>'


class Base(db.Model):
    __abstract__ = True
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    date_modified = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    security_key = db.Column(db.String(128))


class Collection(Base):
    __tablename__ = 'collections'
    name = db.Column(db.String(128), default='My collection', nullable=False)
    data = db.Column(JSON, default='{}', nullable=False)

    def __repr__(self):
        return f'<collection:{self.id}>'
