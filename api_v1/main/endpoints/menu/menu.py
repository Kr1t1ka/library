import datetime

from api_v1.main import db


class Menu(db.Model):
    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, default='default_name')
    text = db.Column(db.String(5000), nullable=False, default='default_text')
    added = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    active = db.Column(db.Boolean, nullable=False, default=True)
    author = db.Column(db.String, nullable=False, default='test_user')

    def __repr__(self):
        return '<Menu %r>' % self.id


class Inheritances(db.Model):
    __tablename__ = "inheritances"

    id_inher = db.Column(db.Integer, primary_key=True)

    menu_id_ancestor = db.Column(db.Integer, db.ForeignKey('menu.id'))
    menu_inher_ancestor = db.relationship('Menu', foreign_keys=[menu_id_ancestor])

    menu_id_descendant = db.Column(db.Integer, db.ForeignKey('menu.id'))
    menu_inher_descendant = db.relationship('Menu', foreign_keys=[menu_id_descendant])

    def __repr__(self):
        return '<Inheritances %r>' % self.id_inher
