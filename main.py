from sweater import app

'''
@app.route('/')
def index():
    conn = psycopg2.connect(database="ISOBN", user="postgres",
                            password="S123456s", host="localhost",
                            port="5432")
    cur = conn.cursor()

    cur.execute(SELECT * FROM offers)

    data = cur.fetchall()

    cur.close()
    cur = conn.cursor()

    cur.execute(SELECT * FROM offers
                   WHERE id = offer_id)
    b_data = cur.fetchall()
    print(b_data)

    cur.close()
    conn.close()
    return render_template('index.html', title="Курсовая", data=data, b_data=b_data)

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    conn = psycopg2.connect(database="ISOBN", user="postgres",
                            password="S123456s", host="localhost",
                            port="5432")
    cur = conn.cursor()
    username = request.form['username']
    password = request.form['password']
    admin = False

    cur.execute(INSERT INTO users \
    (username, password, admin) VALUES (%s, %s, %s),
    (username, password, admin))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/booking', methods=['POST', 'GET'])
def booking():
    conn = psycopg2.connect(database="ISOBN", user="postgres",
                            password="S123456s", host="localhost",
                            port="5432")
    cur = conn.cursor()
    date_min = request.form['date_min']
    date_max = request.form['date_max']

    cur.execute(INSERT INTO b_offers \
    (date_min, date_max) VALUES (%s, %s),
    (date_min, date_max))

    conn.commit()
    cur.close()

    cur = conn.cursor()
    cur.execute(UPDATE offers\
    SET booking = True)

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/create', methods=['POST', 'GET'])
def create():
    conn = psycopg2.connect(database="ISOBN", user="postgres",
                            password="S123456s", host="localhost",
                            port="5432")
    cur = conn.cursor()
    room_num = request.form['room_num']
    area = request.form['area']
    floor = request.form['floor']
    address = request.form['address']
    price = request.form['price']
    publ_date = date.today()
    city = request.form['city']
    booking = False


    cur.execute(INSERT INTO offers \
    (room_num, area, floor, address, price, publ_date, city, booking) VALUES (%s, %s, %s, %s, %s, %s, %s, %s),
    (room_num, area, floor, address, price, publ_date, city, booking))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/update_list', methods=['POST', 'GET'])
def update_list():
    conn = psycopg2.connect(database="ISOBN", user="postgres",
                            password="S123456s", host="localhost",
                            port="5432")
    cur = conn.cursor()

    min_price = request.form['min_p']
    max_price = request.form['max_p']
    room = request.form['roomCheck']
    min_area = request.form['min_s']
    max_area = request.form['max_s']
    city = request.form['cityCheck']
    select_date = request.form['select_date']
    booking_check = request.form['bookingCheck']

    print(min_price)
    print(max_price)
    print(room)
    print(min_area)
    print(max_area)
    print(city)
    print(select_date)
    print(booking_check)

    cur.execute(SELECT * FROM offers \
                WHERE (price > %s AND price < %s) AND \
                      (room_num = %s) AND \
                      (area > %s AND area < %s) AND \
                      (city = %s) AND \
                      (publ_date = %s) AND \
                      (booking = %s);, (min_price, max_price, room, min_area, max_area, city, select_date, booking_check))

    data = cur.fetchall()
    print(data)

    conn.commit()

    cur.close()
    conn.close()
    return render_template('index.html', title="Курсовая", data=data)

@app.route('/delete', methods=['POST'])
def delete():
    conn = psycopg2.connect(database="ISOBN", user="postgres",
                            password="S123456s", host="localhost",
                            port="5432")
    cur = conn.cursor()

    for getid in request.form.getlist('mycheckbox'):
        print(getid)
        cur.execute('DELETE FROM offers WHERE id = {0}'.format(getid))
        conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('index'))



@app.route('/registr', methods=['POST', 'GET'])
def registr():
    print(url_for('registr'))
    return render_template('registr.html', title="Регистрация")


@app.route('/autorizathion')
def autorizathion():
    print(url_for('autorizathion'))
    return render_template('autorizathion.html', title="Авторизация")


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    print(url_for('submit'))
    return render_template('submit.html', title="Submit")

'''
if __name__ == '__main__':
    app.run(debug=True)

