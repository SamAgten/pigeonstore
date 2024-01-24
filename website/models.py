from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150))
    pigeon_coins = db.Column("pigeon_coins", db.Integer)
    orders = db.relationship('Order', backref='user', passive_deletes=True)

    def __init__(self, name, email, password, coins):
        self.name = name
        self.email = email
        self.password = password
        self.pigeon_coins = coins

class Pigeon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Integer)
    number = db.Column(db.Integer)
    info = db.Column(db.String(150))



    def __init__(self, name, number, price, info):
        self.name = name
        self.number = number
        self.price = price
        self.info = info

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pigeon = db.Column(db.Integer, db.ForeignKey('pigeon.id', ondelete="CASCADE"))
    quantity = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))

    def __init__(self, pigeon, quantity, user):
        self.pigeon = pigeon
        self.quantity = quantity
        self.owner = user