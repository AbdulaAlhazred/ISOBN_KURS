from datetime import date

import sqlsession
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy.session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select, or_, and_

from sweater import app, db
from sweater.models import User, Offers, OffersBooking


@app.route('/', methods=['GET', 'POST'])
def index():
    f_city = []
    f_num = []
    data = Offers.query.all()
    filter_city = Offers.query.with_entities(db.distinct(Offers.city)).all()
    filter_room_num = Offers.query.with_entities(db.distinct(Offers.room_num)).all()
    for i in filter_room_num:
        i = str(i)
        i = i.replace("(", "")
        i = i.replace(")", "")
        i = i.replace(",", "")
        f_num.append(i)
    for k in filter_city:
        s1="".join(c for c in k if c.isalpha())
        f_city.append(s1)
    print(f_num)

    bookingData = OffersBooking.query.all()

    return render_template('index.html', title="Курсовая", data=data, f_city=f_city, f_num=f_num, bookingData=bookingData)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/booking', methods=['GET', 'POST'])
@login_required
def create_booking_list():
    f_city = []
    f_num = []
    data = Offers.query.all()
    filter_city = Offers.query.with_entities(db.distinct(Offers.city)).all()
    filter_room_num = Offers.query.with_entities(db.distinct(Offers.room_num)).all()
    for i in filter_room_num:
        i = str(i)
        i = i.replace("(", "")
        i = i.replace(")", "")
        i = i.replace(",", "")
        f_num.append(i)
    for k in filter_city:
        s1 = "".join(c for c in k if c.isalpha())
        f_city.append(s1)

    if request.method == "POST":
        data = []
        for getid in request.form.getlist('checkID'):
            date1 = request.form.get('date_min')
            date2 = request.form.get('date_max')
            getID = getid
            userID = current_user.id
            print(date1)
            print(date2)
            booking_ofer = OffersBooking(date_min=date1, date_max=date2, offer_id=getID, user_id=userID)
            db.session.add(booking_ofer)
            Offers.query.filter(Offers.id == getid).update({'booking': True})

        db.session.commit()

        try:
            data = Offers.query.all()
        except:
            print("[INFO] Ошибка чтения данных")

        return render_template('index.html', data=data)
    elif request.method == "GET":
        data = Offers.query.all()
        return render_template('booking.html', data=data, f_city=f_city, f_num=f_num)
    else:
        return render_template('booking.html')

@app.route('/sort', methods=['GET', 'POST'])
def sort():
    f_city = []
    f_num = []
    data = Offers.query.all()
    filter_city = Offers.query.with_entities(db.distinct(Offers.city)).all()
    filter_room_num = Offers.query.with_entities(db.distinct(Offers.room_num)).all()
    for i in filter_room_num:
        i = str(i)
        i = i.replace("(", "")
        i = i.replace(")", "")
        i = i.replace(",", "")
        f_num.append(i)
    for k in filter_city:
        s1 = "".join(c for c in k if c.isalpha())
        f_city.append(s1)

    sort_msg = request.form.get("sort_msg")
    if sort_msg == "По дате публикации":
        data = Offers.query.order_by(Offers.publ_date).all()
    elif sort_msg == "По цене":
        data = Offers.query.order_by(Offers.price).all()
    elif sort_msg == "По кол-ву комнат":
        data = Offers.query.order_by(Offers.room_num).all()
    else:
        data = Offers.query.all()

    bookingData = OffersBooking.query.all()

    return render_template('index.html', data=data, f_city=f_city, f_num=f_num, bookingData=bookingData)

@app.route('/login', methods=['GET', 'POST'])
def login():
    f_city = []
    f_num = []
    data = Offers.query.all()
    filter_city = Offers.query.with_entities(db.distinct(Offers.city)).all()
    filter_room_num = Offers.query.with_entities(db.distinct(Offers.room_num)).all()
    for i in filter_room_num:
        i = str(i)
        i = i.replace("(", "")
        i = i.replace(")", "")
        i = i.replace(",", "")
        f_num.append(i)
    for k in filter_city:
        s1 = "".join(c for c in k if c.isalpha())
        f_city.append(s1)

    username = request.form.get('username')
    password = request.form.get('password')

    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            rm = True if request.form.get('remainme') else False
            login_user(user, remember=rm)
            data = Offers.query.all()
            return render_template('index.html', data=data, f_city=f_city, f_num=f_num)
        else:
            flash('Введите верный логин и пароль!')
    else:
        flash('Введите логин и пароль!')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('sPassword')

    if request.method == "POST":
        if not (username or password or password2):
            flash('Заполните все необходимые поля!')
        elif password != password2:
            flash('Пароли не совпадают!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(username=username, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('index'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)

    return response

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "POST":
        room_num = request.form.get('room_num')
        area = request.form.get('area')
        floor = request.form.get('floor')
        address = request.form.get('address')
        price = request.form.get('price')
        publ_date = date.today()
        city = request.form.get('city')
        booking = False

        offer = Offers(room_num=room_num,
                       area=area,
                       floor=floor,
                       address=address,
                       price=price,
                       publ_date=publ_date,
                       city=city,
                       booking=booking)

        try:
            db.session.add(offer)
            db.session.commit()
            return redirect('/')
        except:
            return '[INFO] Произошла ошибка при создании поста'
    else:
        return render_template('create.html')

@app.route('/create_list', methods=['GET', 'POST'])
@login_required
def create_list():
    """session: SQLSession = Session()"""
    global bookingData
    global min_price
    global max_price

    message = ''

    fil_city = []
    f_num = []
    data = Offers.query.all()
    filter_city = Offers.query.with_entities(db.distinct(Offers.city)).all()
    filter_room_num = Offers.query.with_entities(db.distinct(Offers.room_num)).all()
    for i in filter_room_num:
        i = str(i)
        i = i.replace("(", "")
        i = i.replace(")", "")
        i = i.replace(",", "")
        f_num.append(i)
    for k in filter_city:
        s1 = "".join(c for c in k if c.isalpha())
        fil_city.append(s1)

    min_price = request.form.get('min_p')
    max_price = request.form.get('max_p')
    room = request.form.get('roomCheck')
    min_area = request.form.get('min_s')
    max_area = request.form.get('max_s')
    f_city = request.form.get('cityCheck')
    select_date = request.form.get('select_date')
    booking_check = request.form.get('bookingCheck')

    t = (min_price and max_price and room and min_area and max_area and f_city and select_date)
    print(t)

    if t:
        price = Offers.price
        oRoom = Offers.room_num
        area = Offers.area
        oCity = Offers.city
        oDate = Offers.publ_date
        data = Offers.query.filter(and_(price > min_price, price < max_price, oRoom == room, area > min_area, area < max_area, oCity == f_city, oDate == select_date))
    else:
        message = "Введите все значения, необходимые для фильтрации"

    try:
        bookingData = OffersBooking.query.all()
    except:
        print("[INFO] Ошибка чтения данных")

    return render_template('index.html', data=data, message=message, bookingData=bookingData, f_city=fil_city, f_num=f_num)



@app.route('/delete', methods=['POST'])
@login_required
def delete():
    if request.method == "POST":
        for getid in request.form.getlist('mycheckbox'):
            print(getid)
            Offers.query.filter(Offers.id == getid).delete()

        db.session.commit()
        data = Offers.query.all()
        return render_template('index.html', data=data)
    else:
        data = Offers.query.all()
        return render_template('index.html', data=data)