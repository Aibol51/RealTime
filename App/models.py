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
    superuser = db.Column(db.Integer, default=0)

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(32), nullable=False)
    img = db.Column(db.String(64), default='img/default_item.png')
    detail_info = db.Column(db.Text, default='None info...')
    view_num = db.Column(db.Integer, default=0)
    requests = db.relationship('Request', backref='requests')
    create_time = db.Column(db.String(32), nullable=False,
                            default=str(datetime.now())[:str(datetime.now()).rfind('.'):])


class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact = db.Column(db.String(64), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    objective_item = db.Column(db.Integer, db.ForeignKey('item.id'))
    create_time = db.Column(db.String(32), nullable=False,
                            default=str(datetime.now())[:str(datetime.now()).rfind('.'):])

class About(db.Model):
    __tablename__ = 'about'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(64), nullable=False)
    img1 = db.Column(db.String(64), nullable=False)
    img2 = db.Column(db.String(64), nullable=False)
    img3 = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text)

class Statistics(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_addr = db.Column(db.String(64), nullable=False)
    create_time = db.Column(db.String(32), nullable=False,
                            default=str(datetime.now())[:str(datetime.now()).find(' ')])

class Visit(db.Model):
    __tablename__ = 'visit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    visit_num = db.Column(db.Integer)
    clean_time = db.Column(db.String(32), nullable=False,
                           default=str(datetime.now())[:str(datetime.now()).find(' ')])