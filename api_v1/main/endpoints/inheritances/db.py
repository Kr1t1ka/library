import datetime

from api_v1.main import db


class Inheritances(db.Model):
    __tablename__ = "inheritances"

    id_inher = db.Column(db.Integer, primary_key=True)
    menu_id_ancestor = db.Column(db.Integer, db.ForeignKey('menu.id'))
    menu_id_descendant = db.Column(db.Integer, db.ForeignKey('menu.id'))
    reversible = db.Column(db.Boolean, nullable=False, default=True)
    added = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    active = db.Column(db.Boolean, nullable=False, default=True)
    author = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Inheritances %r>' % self.id_inher