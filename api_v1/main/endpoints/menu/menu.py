import datetime

from api_v1.main import db


#TODO: добавить метаданные:
# 1 - кто удалил
# 2 - кто последний изменил
# 3 - сколько раз изменили
# 4 - когда именяли
# 5 - предыдущая версия текста (возможно не одна)
# 6 - ...


class Menu(db.Model):
    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    inheritances = db.relationship("Inheritances", backref="menu", lazy=False)
    name = db.Column(db.String(120), nullable=False, default='default_name')
    text = db.Column(db.String(10000), nullable=False, default='default_text')
    added = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    active = db.Column(db.Boolean, nullable=False, default=True)
    author = db.Column(db.String, nullable=False, default='test_user')

    def __repr__(self):
        return '<Menu %r>' % self.id


class Inheritances(db.Model):
    __tablename__ = "inheritances"

    id_inher = db.Column(db.Integer, primary_key=True)
    menu_id_ancestor = db.Column(db.Integer, db.ForeignKey('menu.id'))
    menu_id_descendant = db.Column(db.Integer)
    added = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    active = db.Column(db.Boolean, nullable=False, default=True)
    author = db.Column(db.String, nullable=False, default='test_user')

    def __repr__(self):
        return '<Inheritances %r>' % self.id_inher
