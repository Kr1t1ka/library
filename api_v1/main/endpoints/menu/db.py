import datetime

from api_v1.main import db


class Menu(db.Model):
    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), default='default_name')
    text = db.Column(db.String(10000), default='default_text')
    added = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    active = db.Column(db.Boolean, nullable=False, default=True)
    author_id = db.Column(db.Integer, nullable=False, default=0)
    tags = db.Column(db.String(5000), default='нет тегов')
    inheritances = db.relationship('Inheritances',
                                   primaryjoin="or_(Menu.id==Inheritances.menu_id_descendant, Menu.id==Inheritances.menu_id_ancestor)",
                                   lazy='dynamic')
    attachment = db.relationship('Attachment',
                                 primaryjoin="Menu.id==Attachment.menu_id",
                                 lazy='dynamic')

    def __repr__(self):
        return '<Menu %r>' % self.id


class Attachment(db.Model):
    __tablename__ = 'attachment'

    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    vk_active = db.Column(db.Boolean, nullable=False, default=True)
    telegram_active = db.Column(db.Boolean, nullable=False, default=True)
    vk_attachment = db.Column(db.String(120), default='photo-128637216_456239172')
    telegram_attachment = db.Column(db.String(120), default='default_name')

    def __repr__(self):
        return '<Attachment %r>' % self.id
