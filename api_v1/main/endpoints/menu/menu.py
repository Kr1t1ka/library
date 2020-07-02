from api_v1.main import db


class Menu(db.Model):
    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    text = db.Column(db.String(5000), unique=True)

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
