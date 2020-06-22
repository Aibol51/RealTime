from App.ext import db

from datetime import datetime


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    avator = db.Column(db.String(64), default='img/default_avator.png')
    create_time = db.Column(db.String(32), nullable=False,
                            default=str(datetime.now())[:str(datetime.now()).rfind('.'):])
    login_time = db.Column(db.String(32))

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(32), nullable=False)
    img = db.Column(db.String(64), default='img/default_item.png')
    detail_info = db.Column(db.Text, default='None info...')
    view_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.String(32), nullable=False,
                            default=str(datetime.now())[:str(datetime.now()).rfind('.'):])

class About(db.Model):
    __tablename__ = 'about'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)

