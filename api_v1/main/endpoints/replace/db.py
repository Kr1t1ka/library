import datetime

from api_v1.main import db


# TODO: возможно добавить список статей, где используется переменная


class Replace(db.Model):
    __tablename__ = "replace"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.String(120), default='(перменная не определена)')
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    active = db.Column(db.Boolean, nullable=False, default=True)
    author = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Menu %r>' % self.id
