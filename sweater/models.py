from datetime import date

from flask_login import UserMixin

from sweater import db, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(1000), nullable=False)
    admin = db.Column(db.Boolean(), default=False)


class Offers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    room_num = db.Column(db.Integer(), nullable=False)
    area = db.Column(db.Integer(), nullable=False)
    floor = db.Column(db.Integer(), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    publ_date = db.Column(db.Date(), nullable=False, default=date.today())
    city = db.Column(db.String(100), nullable=False)
    booking = db.Column(db.Boolean(), nullable=False, default=False)


class OffersBooking(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date_min = db.Column(db.String(100), nullable=False)
    date_max = db.Column(db.String(100), nullable=False)
    offer_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
