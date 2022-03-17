from flask import Flask, render_template, request, redirect, send_from_directory
import sqlite3
import os
from datetime import date
from dateutil.relativedelta import relativedelta


currentdirectory = os.path.dirname(os.path.abspath(__file__))
# conn = sqlite3.connect('database.db')
# conn.execute('CREATE TABLE items (name TEXT, price INT)')


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def Coffee_shop():
    return render_template('Coffee_shop.html')


@app.route('/Coffee_shop')
def Coffee_shop_():
    return render_template('Coffee_shop.html')


@app.route('/About')
def About():
    return render_template('About.html')


@app.route('/About_')
def About_():
    return render_template('About_.html')


@app.route('/Menu')
def Menu():
    conn = sqlite3.connect('database.db')
    Hot_Drinks = conn.execute("SELECT name,price_s,price_m,price_l FROM Hot_Drinks;")
    imagename__ = conn.execute("SELECT image FROM Hot_Drinks;")
    result = Hot_Drinks.fetchall()

    Soft_Drinks = conn.execute("SELECT name,price_s,price_m,price_l FROM Soft_Drinks;")
    imagename___ = conn.execute("SELECT image FROM Soft_Drinks;")
    result1 = Soft_Drinks.fetchall()

    Meals = conn.execute("SELECT name,price_s,price_m,price_l FROM Meals;")
    imagename____ = conn.execute("SELECT image FROM Meals;")
    result2 = Meals.fetchall()

    Snacks = conn.execute("SELECT name,price_s,price_m,price_l FROM Snacks;")
    imagename_____ = conn.execute("SELECT image FROM Snacks;")
    result3 = Snacks.fetchall()

    return render_template('Menu.html', data=zip(result, imagename__), data1=zip(result1, imagename___),
                           data2=zip(result2, imagename____), data3=zip(result3, imagename_____))


@app.route('/Menu_')
def Menu_():
    conn = sqlite3.connect('database.db')
    Hot_Drinks = conn.execute("SELECT name,price_s,price_m,price_l FROM Hot_Drinks;")
    imagename__ = conn.execute("SELECT image FROM Hot_Drinks;")
    result = Hot_Drinks.fetchall()

    Soft_Drinks = conn.execute("SELECT name,price_s,price_m,price_l FROM Soft_Drinks;")
    imagename___ = conn.execute("SELECT image FROM Soft_Drinks;")
    result1 = Soft_Drinks.fetchall()

    Meals = conn.execute("SELECT name,price_s,price_m,price_l FROM Meals;")
    imagename____ = conn.execute("SELECT image FROM Meals;")
    result2 = Meals.fetchall()

    Snacks = conn.execute("SELECT name,price_s,price_m,price_l FROM Snacks;")
    imagename_____ = conn.execute("SELECT image FROM Snacks;")
    result3 = Snacks.fetchall()

    return render_template('Menu_.html', data=zip(result, imagename__), data1=zip(result1, imagename___),
                           data2=zip(result2, imagename____), data3=zip(result3, imagename_____))


@app.route('/upload001/<filename>')
def send_image____(filename):
    return send_from_directory("Hot_Drinks_images", filename)


@app.route('/upload0012/<filename>')
def send_image_____(filename):
    return send_from_directory("Soft_Drinks_images", filename)


@app.route('/upload00123/<filename>')
def send_image______(filename):
    return send_from_directory("Meals_images", filename)


@app.route('/upload001234/<filename>')
def send_image_______(filename):
    return send_from_directory("Snacks_images", filename)


########################################## Clients #################
@app.route('/Clients')
def Clients():
    status = 'Available'
    conn = sqlite3.connect('database.db')
    headings = ("Table", "Seats", "Location", "Vip")
    table = "SELECT num,seats,location,vip FROM seats WHERE status=?"
    result1 = conn.execute(table, (status,)).fetchall()
    return render_template('Clients.html', headings=headings, data=result1)


########################################## Login/Sign_up #################
message_login = ''
message_signup = ''
email = ''
message_table = ''
message_vip = ''


def email__(email__):
    global email
    email = email__


@app.route('/Login', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':

        if request.form.get("take_table"):
            table_number = request.form["table"]
            status = 'Unavailable'
            if _error_vip_(table_number) == 1 or _error_vip_(table_number) == 0:
                y = """UPDATE seats SET status = ? WHERE num = ?"""
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute(y, (status, table_number,))
                conn.commit()
                return Payment_()

        elif request.form.get("vip_"):
            email_ = get_email()
            vip = request.form["vip"]
            if error_vip_() == 0 and vip == 'Vip':
                today = date.today()
                d1 = today.strftime("%d/%m/%Y")
                end_date = date.today() + relativedelta(years=+1)
                vip = 'vip'
                x = '''INSERT INTO Vip_date(email,vip,current_date,end_date) VALUES(?,?,?,?)'''
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute(x, (email_, vip, d1, end_date))
                conn.commit()
                return Payment_()
            else:
                __vip__()
            return redirect('/Login')

        elif request.form.get("login"):
            _reset_message_signup_()
            conn = sqlite3.connect('database.db')
            email = request.form["email"]
            email__(email)
            password = request.form["pswd"]
            if check_login_email(email) == 0 or check_login(email, password) == 0:
                error_login()
            else:
                _reset_message_login_()
                position = "SELECT employee FROM Login WHERE email=? and pass=?"
                result = conn.execute(position, (email, password,)).fetchone()
                if result == ('Employee',):
                    return Baristas()
                elif result == ('Admin',):
                    return Admin()
                elif result == ('Customer',):
                    return Clients()
            return redirect('/Login')

        elif request.form.get("sign_up"):
            conn = sqlite3.connect('database.db')
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email_"]
            password = request.form["pswd_"]
            if check_login_email(email) == 1 or check_login(email, password) == 1:
                error_signup()
            else:
                _Success_message_signup_()
                customer = 'Customer'
                cursor = conn.cursor()
                x = '''INSERT INTO Login(first_name,last_name,email,pass,birth_date,id,employee) VALUES(?,?,?,?,?,?,?)'''
                cursor.execute(x, (first_name, last_name, email, password, ' ', ' ', customer))
                conn.commit()
            return redirect('/Login')

        elif request.form.get("submit"):
            table__ = get_table_number()
            card_number = request.form["card_number"]
            card_holder = request.form["card_holder"]
            cvv = request.form["cvv"]
            # if len(card_number) < 16 or len(cvv) < 3 or card_number == '' or card_holder == '' or cvv == '':
            #     __error__()
            # else:
            #     success()
            return Clients()

    else:
        return render_template('Login.html', message=get_message_login(), message_=get_message_signup(),
                               message__=get_message_table(), message___=get_message_vip())


def get_message_vip():
    global message_vip
    return message_vip


def error_vip_():
    g = 0
    email_ = get_email()
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    conn = sqlite3.connect('database.db')
    x = "SELECT email FROM Vip_date"
    x_ = conn.execute(x)
    for row in x_:
        if row == (email_,):
            g = 1
            break

    if g == 1:
        y = "SELECT end_date FROM Vip_date"
        y_ = conn.execute(y)
        for row in y_:
            if row <= (d1,):
                return 1
                break
    return 0


def _error_vip_(num):
    g = 0
    t = 0
    global message_vip
    conn = sqlite3.connect('database.db')
    x = "SELECT num FROM seats"
    x_ = conn.execute(x)
    for row in x_:
        if row == (num,):
            g = 1
            break

    if g == 1:
        z = "SELECT vip FROM seats WHERE num = ?"
        z_ = conn.execute(z, (num,)).fetchone()
        if z_ == ('Yes',):
            t = 1

        if t == 1:
            if error_vip_() == 1:
                message_vip = 'success'
                return 1
            else:
                message_vip = 'You dont have Vip'
                return -1
        else:
            message_vip = 'success'
            return 0


def __vip__():
    global message_vip
    message_vip = 'You have vip'


def error_table():
    conn = sqlite3.connect('database.db')
    x = "SELECT status FROM seats"
    x_ = conn.execute(x)
    for row in x_:
        if row == ('Available',):
            return 1
            break
    return 0


def error_table_():
    global message_table
    message_table = 'Invalid input'


def get_message_table():
    global message_table
    return message_table


def reset_message_table():
    global message_table
    message_table = ''


def get_email():
    global email
    return email


def get_message_signup():
    global message_signup
    return message_signup


def error_signup():
    global message_signup
    message_signup = 'Invalid input'


def _Success_message_signup_():
    global message_signup
    message_signup = 'Success'


def _reset_message_signup_():
    global message_signup
    message_signup = ''


def get_message_login():
    global message_login
    return message_login


def error_login():
    global message_login
    message_login = 'Invalid input'


def _reset_message_login_():
    global message_login
    message_login = ''


def check_login_email(email):
    conn = sqlite3.connect('database.db')
    x = "SELECT email FROM Login"
    x_ = conn.execute(x)
    for row in x_:
        print(row)
        if row == (email,):
            return 1
            break
    return 0


def check_login(email, pass_):
    conn = sqlite3.connect('database.db')
    x = "SELECT pass FROM Login WHERE email = ?"
    x_ = conn.execute(x, (email,))
    for row in x_:
        if row == (pass_,):
            return 1
            break
    return 0


########################################## Admin #################
@app.route('/Admin')
def Admin():
    return render_template('Admin.html')


########################################## Baristas #################
@app.route('/Baristas')
def Baristas():
    conn = sqlite3.connect('database.db')
    headings = ("Table", "Order", "Amount", "Size", "Price", "Total")
    order = conn.execute("SELECT table_,table_nodes,flag,total FROM Nodes ORDER BY table_ ASC;")
    result = order.fetchall()
    table = conn.execute("SELECT choose,amount,size_,price FROM Take_order ORDER BY table_ ASC;")
    result1 = table.fetchall()
    return render_template('Baristas.html', headings=headings, data=zip(result1, result), message=_get__message_())


############################################### Payment ################################
message_payment = ''


# @app.route('/Payment')
def Payment():
    return render_template('Payment.html')


@app.route('/Login')
def Payment_():
    return render_template('Payment_.html')


############################################### Sign_Up ################################
message_ = ''


@app.route('/New_Employee', methods=['POST', 'GET'])
def New_Employee():
    if request.method == 'POST':

        if request.form.get("Add"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            password = request.form["pass"]
            birth_date = request.form["birth_date"]
            id = request.form["id"]
            employee = 'Employee'
            if first_name == '' or last_name == '' or email == '' or password == '' or birth_date == '' or id == '' or int(
                    id) < 0:
                _error_()
            else:
                reset__message__()
                conn = sqlite3.connect(currentdirectory + '\database.db')
                cursor = conn.cursor()
                x = '''INSERT INTO Login(first_name,last_name,email,pass,birth_date,id,employee) VALUES(?,?,?,?,?,?,?)'''
                cursor.execute(x, (first_name, last_name, email, password, birth_date, id, employee))
                conn.commit()
            return redirect('/New_Employee')

        elif request.form.get("Delete"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            password = request.form["pass"]
            birth_date = request.form.get("birth_date")
            id = request.form["id"]
            employee = 'Employee'
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            if first_name == '' or last_name == '' or email == '' or password == '' or birth_date == '' or id == '' or int(
                    id) < 0:
                _error_()
            else:
                reset__message__()
                delete = "DELETE FROM Login WHERE first_name=? and last_name=? and email=? and pass=? and birth_date=? and id=? and employee=?"
                # get_message_delete__(name, price_s, price_m, price_l)
                cursor.execute(delete, (first_name, last_name, email, password, birth_date, id, employee,))
                conn.commit()
            return redirect('/New_Employee')

        elif request.form.get("Back"):
            reset__message__()
            return Admin()

    else:
        employee_ = 'Employee'
        headings = ("First_Name", "Last_Name", "Email", "Password", "Birth_Date", "Id")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        employee = "SELECT first_name,last_name,email,pass,birth_date,id FROM Login WHERE employee=?"
        result = cursor.execute(employee, (employee_,)).fetchall()
        return render_template('Admin-New_employee.html', headings=headings, data=result, message=_get_message_())


@app.route('/upload00/<filename>')
def send_image(filename):
    return send_from_directory("Thumbnail", filename)


def _error_():
    global message_
    message_ = 'Invalid price or Empty field'


def reset__message__():
    global message_
    message_ = ''


def _get_message_():
    global message_
    return message_


############################################### Hot_Drinks ################################
message_Hot_Drinks = ''


@app.route('/Hot_Drinks_data', methods=['POST', 'GET'])
def Hot_Drinks_data():
    if request.method == 'POST':

        if request.form.get("Add"):
            target = os.path.join(APP_ROOT, 'Hot_Drinks_images/')
            name = request.form["name"]
            price_s = request.form["price-s"]
            price_m = request.form["price-m"]
            price_l = request.form["price-l"]
            for image in request.files.getlist("image"):
                filename = image.filename
                if filename != '':
                    destination = "/".join([target, filename])
                    image.save(destination)
            if name == '' or price_s == '' or price_m == '' or price_l == '' or int(price_s) < 0 or int(
                    price_m) < 0 or int(price_l) < 0 or filename == '':
                error_Hot_Drinks()
            else:
                reset_message()
                conn = sqlite3.connect(currentdirectory + '\database.db')
                cursor = conn.cursor()
                x = '''INSERT INTO Hot_Drinks(name,price_s,price_m,price_l,image) VALUES(?,?,?,?,?)'''
                cursor.execute(x, (name, price_s, price_m, price_l, filename))
                conn.commit()
            return redirect('/Hot_Drinks_data')

        elif request.form.get("Delete"):
            name = request.form["name"]
            price_s = request.form["price-s"]
            price_m = request.form["price-m"]
            price_l = request.form["price-l"]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            if name == '' or price_s == '' or price_m == '' or price_l == '' or int(price_s) < 0 or int(
                    price_m) < 0 or int(price_l) < 0:
                error_Hot_Drinks()
            else:
                reset_message()
                delete = "DELETE FROM Hot_Drinks WHERE name=? and price_s=? and price_m=? and price_l=?"
                image = "SELECT image FROM Hot_Drinks WHERE name=? and price_s=? and price_m=? and price_l=?"
                image_ = cursor.execute(image, (name, price_s, price_m, price_l,))
                t = image_.fetchone()
                if t != None:
                    file_path = 'Hot_Drinks_images/' + t[0]
                    os.remove(file_path)
                get_message_delete(name, price_s, price_m, price_l)
                cursor.execute(delete, (name, price_s, price_m, price_l,))
                conn.commit()
            return redirect('/Hot_Drinks_data')

        elif request.form.get("Update"):
            name = request.form["name"]
            update = "UPDATE Hot_Drinks SET name = ? , price_s = ?, price_m = ?, price_l = ? WHERE name =?"
            newname = request.form["name"]
            newprice_s = request.form["price-s"]
            newprice_m = request.form["price-m"]
            newprice_l = request.form["price-l"]
            conn = sqlite3.connect('database.db')
            get_message_update(name)
            if newprice_s == '' or newprice_m == '' or newprice_l == '' or int(newprice_s) < 0 or int(
                    newprice_m) < 0 or int(newprice_l) < 0:
                error_Hot_Drinks()
            else:
                reset_message()
                cursor = conn.cursor()
                cursor.execute(update, (newname, newprice_s, newprice_m, newprice_l, name,))
                conn.commit()
            return redirect('/Hot_Drinks_data')

        elif request.form.get("Back"):
            reset_message()
            return Admin()

    else:
        headings = ("Hot_Drinks", "S-Price", "M-Price", "L-Price", "Image")
        conn = sqlite3.connect('database.db')
        Hot_Drinks = conn.execute("SELECT name,price_s,price_m,price_l FROM Hot_Drinks;")
        imagename__ = conn.execute("SELECT image FROM Hot_Drinks;")
        result = Hot_Drinks.fetchall()
        return render_template('Admin-Hot_Drinks.html', headings=headings, data=zip(result, imagename__),
                               message=get_message())


@app.route('/upload0/<filename>')
def send_image_Hot_Drinks(filename):
    return send_from_directory("Hot_Drinks_images", filename)


def reset_message():
    global message_Hot_Drinks
    message_Hot_Drinks = ''


def error_Hot_Drinks():
    global message_Hot_Drinks
    message_Hot_Drinks = 'Invalid price or Empty field'


def get_message():
    return message_Hot_Drinks


def get_message_delete(name, price_s, price_m, price_l):
    global message_Hot_Drinks
    flag = 1
    temp_s = 1
    temp_m = 1
    temp_l = 1
    conn = sqlite3.connect('database.db')
    Hot_Drinks_name = conn.execute("SELECT name FROM Hot_Drinks;")
    result_name = Hot_Drinks_name.fetchall()
    for row_name in result_name:
        if row_name == (name,):
            flag = 0
            break
        else:
            flag = 1

    Hot_Drinks_price_s = conn.execute("SELECT price_s FROM Hot_Drinks;")
    result_price_s = Hot_Drinks_price_s.fetchall()
    for row_price in result_price_s:
        if str(row_price[0]) == price_s:
            temp_s = 0
            break
        else:
            temp_s = 1

    Hot_Drinks_price_m = conn.execute("SELECT price_m FROM Hot_Drinks;")
    result_price_m = Hot_Drinks_price_m.fetchall()
    for row_price in result_price_m:
        if str(row_price[0]) == price_m:
            temp_m = 0
            break
        else:
            temp_m = 1

    Hot_Drinks_price_l = conn.execute("SELECT price_l FROM Hot_Drinks;")
    result_price_l = Hot_Drinks_price_l.fetchall()
    for row_price in result_price_l:
        if str(row_price[0]) == price_l:
            temp_l = 0
            break
        else:
            temp_l = 1

    if temp_s == 0 and temp_m == 0 and temp_l == 0 and flag == 0:
        message_Hot_Drinks = ''
    else:
        message_Hot_Drinks = "Wrong coffee or price"


def get_message_update(name):
    global message_Hot_Drinks
    helper = 1
    conn = sqlite3.connect('database.db')
    Hot_Drinks_name = conn.execute("SELECT name FROM Hot_Drinks;")
    result = Hot_Drinks_name.fetchall()
    for row in result:
        if row == (name,):
            helper = 0
            break
        else:
            helper = 1

    if helper == 1:
        message_Hot_Drinks = "Wrong coffee name"
    else:
        message_Hot_Drinks = ''


############################################### Soft_Drinks ################################
message_Soft_Drinks = ''


@app.route('/Soft_Drinks_data', methods=['POST', 'GET'])
def Soft_Drinks_data():
    if request.method == 'POST':

        if request.form.get("Add"):
            target = os.path.join(APP_ROOT, 'Soft_Drinks_images/')
            name = request.form["name"]
            price_s = request.form["price-s"]
            price_m = request.form["price-m"]
            price_l = request.form["price-l"]
            for image in request.files.getlist("image"):
                filename = image.filename
                if filename != '':
                    destination = "/".join([target, filename])
                    image.save(destination)
            if name == '' or price_s == '' or price_m == '' or price_l == '' or int(price_s) < 0 or int(
                    price_m) < 0 or int(price_l) < 0 or filename == '':
                error_Soft_Drinks_()
            else:
                reset_message_()
                conn = sqlite3.connect(currentdirectory + '\database.db')
                cursor = conn.cursor()
                x = '''INSERT INTO Soft_Drinks(name,price_s,price_m,price_l,image) VALUES(?,?,?,?,?)'''
                cursor.execute(x, (name, price_s, price_m, price_l, filename))
                conn.commit()
            return redirect('/Soft_Drinks_data')

        elif request.form.get("Delete"):
            name = request.form["name"]
            price_s = request.form["price-s"]
            price_m = request.form["price-m"]
            price_l = request.form["price-l"]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            if name == '' or price_s == '' or price_m == '' or price_l == '' or int(price_s) < 0 or int(
                    price_m) < 0 or int(price_l) < 0:
                error_Soft_Drinks_()
            else:
                reset_message_()
                delete = "DELETE FROM Soft_Drinks WHERE name=? and price_s=? and price_m=? and price_l=?"
                image = "SELECT image FROM Soft_Drinks WHERE name=? and price_s=? and price_m=? and price_l=?"
                image_ = cursor.execute(image, (name, price_s, price_m, price_l,))
                t = image_.fetchone()
                if t != None:
                    file_path = 'Soft_Drinks_images/' + t[0]
                    os.remove(file_path)
                get_message_delete_(name, price_s, price_m, price_l)
                cursor.execute(delete, (name, price_s, price_m, price_l,))
                conn.commit()
            return redirect('/Soft_Drinks_data')

        elif request.form.get("Update"):
            name = request.form["name"]
            update = "UPDATE Soft_Drinks SET name = ? , price_s = ?, price_m = ?, price_l = ? WHERE name =?"
            newname = request.form["name"]
            newprice_s = request.form["price-s"]
            newprice_m = request.form["price-m"]
            newprice_l = request.form["price-l"]
            conn = sqlite3.connect('database.db')
            get_message_update_(name)
            if newprice_s == '' or newprice_m == '' or newprice_l == '' or int(newprice_s) < 0 or int(
                    newprice_m) < 0 or int(newprice_l) < 0:
                error_Soft_Drinks_()
            else:
                reset_message_()
                cursor = conn.cursor()
                cursor.execute(update, (newname, newprice_s, newprice_m, newprice_l, name,))
                conn.commit()
            return redirect('/Soft_Drinks_data')

        elif request.form.get("Back"):
            reset_message_()
            return Admin()

    else:
        headings = ("Soft Drinks", "S-Price", "M-Price", "L-Price", "Images")
        conn = sqlite3.connect('database.db')
        Soft_Drinks = conn.execute("SELECT name,price_s,price_m,price_l FROM Soft_Drinks;")
        imagename__ = conn.execute("SELECT image FROM Soft_Drinks;")
        result = Soft_Drinks.fetchall()
        return render_template('Admin-Soft_Drinks.html', headings=headings, data=zip(result, imagename__),
                               message=get_message_())


@app.route('/upload1/<filename>')
def send_image_Soft_Drinks(filename):
    return send_from_directory("Soft_Drinks_images", filename)


def reset_message_():
    global message_Soft_Drinks
    message_Soft_Drinks = ''


def error_Soft_Drinks_():
    global message_Soft_Drinks
    message_Soft_Drinks = 'Invalid price or Empty field'


def get_message_():
    return message_Soft_Drinks


def get_message_delete_(name, price_s, price_m, price_l):
    global message_Soft_Drinks
    flag = 1
    temp_s = 1
    temp_m = 1
    temp_l = 1
    conn = sqlite3.connect('database.db')
    Soft_Drinks_name = conn.execute("SELECT name FROM Soft_Drinks;")
    result_name = Soft_Drinks_name.fetchall()
    for row_name in result_name:
        if row_name == (name,):
            flag = 0
            break
        else:
            flag = 1

    Soft_Drinks_price_s = conn.execute("SELECT price_s FROM Soft_Drinks;")
    result_price_s = Soft_Drinks_price_s.fetchall()
    for row_price in result_price_s:
        if str(row_price[0]) == price_s:
            temp_s = 0
            break
        else:
            temp_s = 1

    Soft_Drinks_price_m = conn.execute("SELECT price_m FROM Soft_Drinks;")
    result_price_m = Soft_Drinks_price_m.fetchall()
    for row_price in result_price_m:
        if str(row_price[0]) == price_m:
            temp_m = 0
            break
        else:
            temp_m = 1

    Soft_Drinks_price_l = conn.execute("SELECT price_l FROM Soft_Drinks;")
    result_price_l = Soft_Drinks_price_l.fetchall()
    for row_price in result_price_l:
        if str(row_price[0]) == price_l:
            temp_l = 0
            break
        else:
            temp_l = 1

    if temp_s == 0 and temp_m == 0 and temp_l == 0 and flag == 0:
        message_Soft_Drinks = ''
    else:
        message_Soft_Drinks = "Wrong coffee or price"


def get_message_update_(name):
    global message_Soft_Drinks
    helper = 1
    conn = sqlite3.connect('database.db')
    Soft_Drinks_name = conn.execute("SELECT name FROM Soft_Drinks;")
    result = Soft_Drinks_name.fetchall()
    for row in result:
        if row == (name,):
            helper = 0
            break
        else:
            helper = 1

    if helper == 1:
        message_Soft_Drinks = "Wrong item name"
    else:
        message_Soft_Drinks = ''


############################################### Meals ################################
message_Meals = ''


@app.route('/Meals_data', methods=['POST', 'GET'])
def Meals_data():
    if request.method == 'POST':

        if request.form.get("Add"):
            target = os.path.join(APP_ROOT, 'Meals_images/')
            name = request.form["name"]
            price_s = request.form["price-s"]
            price_m = request.form["price-m"]
            price_l = request.form["price-l"]
            for image in request.files.getlist("image"):
                filename = image.filename
                if filename != '':
                    destination = "/".join([target, filename])
                    image.save(destination)
            if name == '' or price_s == '' or price_m == '' or price_l == '' or int(price_s) < 0 or int(
                    price_m) < 0 or int(price_l) < 0 or filename == '':
                error_Meals_()
            else:
                reset_message__()
                conn = sqlite3.connect(currentdirectory + '\database.db')
                cursor = conn.cursor()
                x = '''INSERT INTO Meals(name,price_s,price_m,price_l,image) VALUES(?,?,?,?,?)'''
                cursor.execute(x, (name, price_s, price_m, price_l, filename))
                conn.commit()
            return redirect('/Meals_data')

        elif request.form.get("Delete"):
            name = request.form["name"]
            price_s = request.form["price-s"]
            price_m = request.form["price-m"]
            price_l = request.form["price-l"]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            if name == '' or price_s == '' or price_m == '' or price_l == '' or int(price_s) < 0 or int(
                    price_m) < 0 or int(price_l) < 0:
                error_Meals_()
            else:
                reset_message__()
                delete = "DELETE FROM Meals WHERE name=? and price_s=? and price_m=? and price_l=?"
                image = "SELECT image FROM Meals WHERE name=? and price_s=? and price_m=? and price_l=?"
                image_ = cursor.execute(image, (name, price_s, price_m, price_l,))
                t = image_.fetchone()
                if t != None:
                    file_path = 'Meals_images/' + t[0]
                    os.remove(file_path)
                get_message_delete__(name, price_s, price_m, price_l)
                cursor.execute(delete, (name, price_s, price_m, price_l,))
                conn.commit()
            return redirect('/Meals_data')

        elif request.form.get("Update"):
            name = request.form["name"]
            update = "UPDATE Meals SET name = ? , price_s = ?, price_m = ?, price_l = ? WHERE name =?"
            newname = request.form["name"]
            newprice_s = request.form["price-s"]
            newprice_m = request.form["price-m"]
            newprice_l = request.form["price-l"]
            conn = sqlite3.connect('database.db')
            get_message_update__(name)
            if newprice_s == '' or newprice_m == '' or newprice_l == '' or int(newprice_s) < 0 or int(
                    newprice_m) < 0 or int(newprice_l) < 0:
                error_Meals_()
            else:
                reset_message__()
                cursor = conn.cursor()
                cursor.execute(update, (newname, newprice_s, newprice_m, newprice_l, name,))
                conn.commit()
            return redirect('/Meals_data')

        elif request.form.get("Back"):
            reset_message__()
            return Admin()

    else:
        headings = ("Meals", "S-Price", "M-Price", "L-Price", "Images")
        conn = sqlite3.connect('database.db')
        Meals = conn.execute("SELECT name,price_s,price_m,price_l FROM Meals;")
        imagename__ = conn.execute("SELECT image FROM Meals;")
        result = Meals.fetchall()
        return render_template('Admin-Meals.html', headings=headings, data=zip(result, imagename__),
                               message=get_message__())


@app.route('/upload2/<filename>')
def send_image_Meals(filename):
    return send_from_directory("Meals_images", filename)


def reset_message__():
    global message_Meals
    message_Meals = ''


def error_Meals_():
    global message_Meals
    message_Meals = 'Invalid price or Empty field'


def get_message__():
    return message_Meals


def get_message_delete__(name, price_s, price_m, price_l):
    global message_Meals
    flag = 1
    temp_s = 1
    temp_m = 1
    temp_l = 1
    conn = sqlite3.connect('database.db')
    Meals_name = conn.execute("SELECT name FROM Meals;")
    result_name = Meals_name.fetchall()
    for row_name in result_name:
        if row_name == (name,):
            flag = 0
            break
        else:
            flag = 1

    Meals_price_s = conn.execute("SELECT price_s FROM Meals;")
    result_price_s = Meals_price_s.fetchall()
    for row_price in result_price_s:
        if str(row_price[0]) == price_s:
            temp_s = 0
            break
        else:
            temp_s = 1

    Meals_price_m = conn.execute("SELECT price_m FROM Meals;")
    result_price_m = Meals_price_m.fetchall()
    for row_price in result_price_m:
        if str(row_price[0]) == price_m:
            temp_m = 0
            break
        else:
            temp_m = 1

    Meals_price_l = conn.execute("SELECT price_l FROM Meals;")
    result_price_l = Meals_price_l.fetchall()
    for row_price in result_price_l:
        if str(row_price[0]) == price_l:
            temp_l = 0
            break
        else:
            temp_l = 1

    if temp_s == 0 and temp_m == 0 and temp_l == 0 and flag == 0:
        message_Meals = ''
    else:
        message_Meals = "Wrong coffee or price"


def get_message_update__(name):
    global message_Meals
    helper = 1
    conn = sqlite3.connect('database.db')
    Meals_name = conn.execute("SELECT name FROM Meals;")
    result = Meals_name.fetchall()
    for row in result:
        if row == (name,):
            helper = 0
            break
        else:
            helper = 1

    if helper == 1:
        message_Meals = "Wrong item name"
    else:
        message_Meals = ''


############################################### Snacks ################################
message_Snacks = ''


@app.route('/Snacks_data', methods=['POST', 'GET'])
def Snacks_data():
    if request.method == 'POST':

        if request.form.get("Add"):
            target = os.path.join(APP_ROOT, 'Snacks_images/')
            name = request.form["name"]
            price_s = request.form["price-s"]
            price_m = request.form["price-m"]
            price_l = request.form["price-l"]
            for image in request.files.getlist("image"):
                filename = image.filename
                if filename != '':
                    destination = "/".join([target, filename])
                    image.save(destination)
            if name == '' or price_s == '' or price_m == '' or price_l == '' or int(price_s) < 0 or int(
                    price_m) < 0 or int(price_l) < 0 or filename == '':
                error_Snacks_()
            else:
                reset_message___()
                conn = sqlite3.connect(currentdirectory + '\database.db')
                cursor = conn.cursor()
                x = '''INSERT INTO Snacks(name,price_s,price_m,price_l,image) VALUES(?,?,?,?,?)'''
                cursor.execute(x, (name, price_s, price_m, price_l, filename))
                conn.commit()
            return redirect('/Snacks_data')

        elif request.form.get("Delete"):
            name = request.form["name"]
            price_s = request.form["price-s"]
            price_m = request.form["price-m"]
            price_l = request.form["price-l"]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            if name == '' or price_s == '' or price_m == '' or price_l == '' or int(price_s) < 0 or int(
                    price_m) < 0 or int(price_l) < 0:
                error_Snacks_()
            else:
                reset_message___()
                delete = "DELETE FROM Snacks WHERE name=? and price_s=? and price_m=? and price_l=?"
                image = "SELECT image FROM Snacks WHERE name=? and price_s=? and price_m=? and price_l=?"
                image_ = cursor.execute(image, (name, price_s, price_m, price_l,))
                t = image_.fetchone()
                if t != None:
                    file_path = 'Snacks_images/' + t[0]
                    os.remove(file_path)
                get_message_delete___(name, price_s, price_m, price_l)
                cursor.execute(delete, (name, price_s, price_m, price_l,))
                conn.commit()
            return redirect('/Snacks_data')

        elif request.form.get("Update"):
            name = request.form["name"]
            update = "UPDATE Snacks SET name = ? , price_s = ?, price_m = ?, price_l = ? WHERE name =?"
            newname = request.form["name"]
            newprice_s = request.form["price-s"]
            newprice_m = request.form["price-m"]
            newprice_l = request.form["price-l"]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            get_message_update___(name)
            if newprice_s == '' or newprice_m == '' or newprice_l == '' or int(newprice_s) < 0 or int(
                    newprice_m) < 0 or int(newprice_l) < 0:
                error_Snacks_()
            else:
                reset_message___()
                cursor.execute(update, (newname, newprice_s, newprice_m, newprice_l, name,))
                conn.commit()
            return redirect('/Snacks_data')

        elif request.form.get("Back"):
            reset_message___()
            return Admin()

    else:
        headings = ("Snacks", "S-Price", "M-Price", "L-Price", "Images")
        conn = sqlite3.connect('database.db')
        Snacks = conn.execute("SELECT name,price_s,price_m,price_l FROM Snacks;")
        imagename__ = conn.execute("SELECT image FROM Snacks;")
        result = Snacks.fetchall()
        return render_template('Admin-Snacks.html', headings=headings, data=zip(result, imagename__),
                               message=get_message___())


@app.route('/upload3/<filename>')
def send_image_Snacks(filename):
    return send_from_directory("Snacks_images", filename)


def reset_message___():
    global message_Snacks
    message_Snacks = ''


def error_Snacks_():
    global message_Snacks
    message_Snacks = 'Invalid price or Empty field'


def get_message___():
    return message_Snacks


def get_message_delete___(name, price_s, price_m, price_l):
    global message_Snacks
    flag = 1
    temp_s = 1
    temp_m = 1
    temp_l = 1
    conn = sqlite3.connect('database.db')
    Snacks_name = conn.execute("SELECT name FROM Snacks;")
    result_name = Snacks_name.fetchall()
    for row_name in result_name:
        if row_name == (name,):
            flag = 0
            break
        else:
            flag = 1

    Snacks_price_s = conn.execute("SELECT price_s FROM Snacks;")
    result_price_s = Snacks_price_s.fetchall()
    for row_price in result_price_s:
        if str(row_price[0]) == price_s:
            temp_s = 0
            break
        else:
            temp_s = 1

    Snacks_price_m = conn.execute("SELECT price_m FROM Snacks;")
    result_price_m = Snacks_price_m.fetchall()
    for row_price in result_price_m:
        if str(row_price[0]) == price_m:
            temp_m = 0
            break
        else:
            temp_m = 1

    Snacks_price_l = conn.execute("SELECT price_l FROM Snacks;")
    result_price_l = Snacks_price_l.fetchall()
    for row_price in result_price_l:
        if str(row_price[0]) == price_l:
            temp_l = 0
            break
        else:
            temp_l = 1

    if temp_s == 0 and temp_m == 0 and temp_l == 0 and flag == 0:
        message_Snacks = ''
    else:
        message_Snacks = "Wrong meal or price"


def get_message_update___(name):
    global message_Snacks
    helper = 1
    conn = sqlite3.connect('database.db')
    Snacks_name = conn.execute("SELECT name FROM Snacks;")
    result = Snacks_name.fetchall()
    for row in result:
        if row == (name,):
            helper = 0
            break
        else:
            helper = 1

    if helper == 1:
        message_Snacks = "Wrong item name"
    else:
        message_Snacks = ''


############################################### seats ################################
message_seats = ''

message_sale = ''


@app.route('/seats_data', methods=['POST', 'GET'])
def seats_data():
    if request.method == 'POST':

        if request.form.get("Update-sale"):
            vip = 'Yes'
            update = "UPDATE Vip SET sale=? WHERE vip =?"
            sale = request.form["sale"]
            conn = sqlite3.connect('database.db')
            if sale == '' or int(sale) < 0:
                error_add_seats_()
            else:
                reset_message____()
                cursor = conn.cursor()
                cursor.execute(update, (sale, vip,))
                conn.commit()
            return redirect('/seats_data')

        elif request.form.get("Add"):
            num = request.form["num"]
            seats = request.form["seats"]
            location = request.form["location"]
            vip = request.form["vip"]
            status = 'Available'
            check = search(num)
            if num == '' or seats == '' or location == '' or vip == '' or int(num) < 0 or int(seats) < 0 or check == 0:
                error_add_seats_()
            else:
                reset_message____()
                conn = sqlite3.connect(currentdirectory + '\database.db')
                cursor = conn.cursor()
                x = "INSERT INTO seats VALUES ({n} ,{p}, '{l}','{v}','{s}')".format(n=num, p=seats, l=location, v=vip,
                                                                                    s=status)
                cursor.execute(x)
                conn.commit()
            return redirect('/seats_data')

        elif request.form.get("Delete"):
            num = request.form["num"]
            seats = request.form["seats"]
            location = request.form["location"]
            vip = request.form["vip"]
            delete = "DELETE FROM seats WHERE num=? and seats=? and location = ? and vip = ?"
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            get_message_delete____(num, seats, location, vip)
            cursor.execute(delete, (num, seats, location, vip,))
            conn.commit()
            return redirect('/seats_data')

        elif request.form.get("Update"):
            num = request.form["num"]
            update = "UPDATE seats SET num = ? , seats = ?, location = ?, vip = ? WHERE num = ?"
            newnum = request.form["num"]
            newseats = request.form["seats"]
            newlocation = request.form["location"]
            newvip = request.form["vip"]
            conn = sqlite3.connect('database.db')
            get_message_update____(num)
            cursor = conn.cursor()
            cursor.execute(update, (newnum, newseats, newlocation, newvip, num,))
            conn.commit()
            return redirect('/seats_data')

        elif request.form.get("Back"):
            reset_message____()
            return Admin()

    else:
        headings = ("Table Number", "Seats", "Location", "Vip")
        conn = sqlite3.connect('database.db')
        table = conn.execute("SELECT num,seats,location,vip FROM seats;")
        result = table.fetchall()
        sale = conn.execute("SELECT sale FROM Vip;")
        result_sale = sale.fetchall()
        return render_template('Admin-seats.html', headings=headings, data=result, data1=result_sale,
                               message=get_message____())


def reset_message____():
    global message_seats
    message_seats = ''


def error_add_seats_():
    global message_seats
    message_seats = 'Invalid input'


def get_message____():
    return message_seats


def get_message_delete____(num, seats, location, vip):
    global message_seats
    flag = 1
    temp = 1
    L = 1
    V = 1
    conn = sqlite3.connect('database.db')

    num_ = conn.execute("SELECT num FROM seats;")
    result_num = num_.fetchall()
    for row in result_num:
        if str(row[0]) == num:
            flag = 0
            break
        else:
            flag = 1

    seats_ = conn.execute("SELECT seats FROM seats;")
    result_seats = seats_.fetchall()
    for row in result_seats:
        if str(row[0]) == seats:
            temp = 0
            break
        else:
            temp = 1

    location_ = conn.execute("SELECT location FROM seats;")
    result_location = location_.fetchall()
    for row in result_location:
        if row == (location,):
            L = 0
            break
        else:
            L = 1

    vip_ = conn.execute("SELECT vip FROM seats;")
    result_vip = vip_.fetchall()
    for row in result_vip:
        if row == (vip,):
            V = 0
            break
        else:
            V = 1

    if temp == 0 and flag == 0 and L == 0 and V == 0:
        message_seats = ''
    else:
        message_seats = "Invalid input"


def get_message_update____(num):
    global message_seats
    helper = 1
    conn = sqlite3.connect('database.db')
    num_table = conn.execute("SELECT num FROM seats;")
    result = num_table.fetchall()
    for row in result:
        if row == (num,):
            helper = 0
            break
        else:
            helper = 1

    if helper == 1:
        message_seats = "Invalid input"
    else:
        message_seats = ''


def search(num):
    helper = 1
    conn = sqlite3.connect('database.db')
    num_table = conn.execute("SELECT num FROM seats;")
    result = num_table.fetchall()
    for row in result:
        if row == (int(num),):
            helper = 0
            break
        else:
            helper = 1

    return helper


################################################## Take_order #################
table_number = ''
_message_ = ''
flag = 0
id = 0
flag__ = 0


@app.route('/Take_order', methods=['POST', 'GET'])
def Take_order():
    if request.method == 'POST':

        if request.form.get("Start_order"):
            _reset_message_()
            global table_number
            table_number = request.form["table"]
            email = request.form["email"]
            if table_number == '':
                __error__()
            else:
                check = check_table()
                if check == 0:
                    f = 1
                    flag_(f)
            return redirect('/Take_order')

        elif request.form.get("Done"):
            table_number = request.form["table"]
            payment = request.form["payment"]
            if table_number == '' or payment == '':
                __error__()
            else:
                _reset_message_()
                if payment == 'Credit Card':
                    __flag__(1)
                    return Payment()
                elif payment == 'Cash':
                    status = 'Available'
                    delete = "DELETE FROM Take_order WHERE table_=?"
                    delete_ = "DELETE FROM Nodes WHERE table_=?"
                    y = """UPDATE seats SET status = ? WHERE num = ?"""
                    conn = sqlite3.connect('database.db')
                    cursor = conn.cursor()
                    cursor.execute(delete, (table_number,))
                    cursor.execute(delete_, (table_number,))
                    cursor.execute(y, (status, table_number,))
                    conn.commit()
                    return Baristas()
            return redirect('/Take_order')

        elif request.form.get("submit"):
            table__ = get_table_number()
            card_number = request.form["card_number"]
            card_holder = request.form["card_holder"]
            cvv = request.form["cvv"]
            if len(card_number) < 16 or len(cvv) < 3 or card_number == '' or card_holder == '' or cvv == '':
                __error__()
            else:
                flag__ = get__flag__()
                if flag__ == 1:
                    success()
                    __flag__(0)
                    status = 'Available'
                    delete = "DELETE FROM Take_order WHERE table_=?"
                    delete_ = "DELETE FROM Nodes WHERE table_=?"
                    y = """UPDATE seats SET status = ? WHERE num = ?"""
                    conn = sqlite3.connect('database.db')
                    cursor = conn.cursor()
                    cursor.execute(delete, (table__,))
                    cursor.execute(delete_, (table__,))
                    cursor.execute(y, (status, table__,))
                    conn.commit()
            return Baristas()

        elif request.form.get("Add"):
            table__ = get_table_number()
            type = request.form.get("sel1")
            choose = request.form.get("sel2")
            amount = request.form["amount"]
            size = request.form["size"]
            price = get_price(type, amount, size, choose)
            status = 'Unavailable'
            id = _id_()
            if type == '' or choose == '' or amount == '' or size == '' or price == '' or int(amount) < 0 or int(
                    price) < 0:
                __error__()
            else:
                _reset_message_()
                conn = sqlite3.connect(currentdirectory + '\database.db')
                cursor = conn.cursor()
                check = check_table()
                if check == 1:
                    table_nodes = "SELECT table_nodes FROM Nodes WHERE table_=?"
                    table_node = conn.execute(table_nodes, (table__,))
                    result = table_node.fetchone()
                    result_ = int(result[0])
                elif check == 0:
                    result_ = 0
                cursor.execute("""INSERT INTO Take_order(table_,type,choose,amount,size_,price) VALUES (?,?,?,?,?,?)""",
                               (table__, type, choose, amount, size, price))
                y = """UPDATE seats SET status = ? WHERE num = ?"""
                cursor.execute(y, (status, table__,))
                table__nodes = 0
                flag = get_flag()
                cursor.execute('INSERT INTO Nodes (table_, table_nodes, flag, id,total) VALUES (?,?,?,?,?)', (table__,
                                                                                                              table__nodes,
                                                                                                              flag,
                                                                                                              id, ''))
                t = """UPDATE Nodes SET table_nodes = ? WHERE table_ = ?"""
                cursor.execute(t, (result_ + 1, table__,))
                f = 0
                flag_(f)
                conn.commit()
            return redirect('/Take_order')

        elif request.form.get("Delete"):
            table = get_table_number()
            type = request.form.get("sel1")
            choose = request.form.get("sel2")
            amount = request.form["amount"]
            size = request.form["size"]
            delete = "DELETE FROM Take_order WHERE table_=? and type=? and choose = ? and amount = ? and size_=?"
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            check = _get_message_delete_(table, type, choose, amount, size)
            if check == 0:
                cursor.execute(delete, (table, type, choose, amount, size,))
                table_nodes = "SELECT table_nodes FROM Nodes WHERE table_=?"
                table_node = conn.execute(table_nodes, (table,))
                result = table_node.fetchone()
                result_ = int(result[0])
                z = """UPDATE Nodes SET table_nodes = ? WHERE table_ = ?"""
                cursor.execute(z, (result_ - 1, table,))
                r = "DELETE FROM Nodes WHERE id = (SELECT MAX(id) FROM Nodes WHERE table_=? ORDER BY table_ ASC);"
                cursor.execute(r, (table,))
            conn.commit()
            return redirect('/Take_order')

        elif request.form.get("Update"):
            table = get_table_number()
            type = request.form.get("sel1")
            choose = request.form.get("sel2")
            update = "UPDATE Take_order SET table_=?,type =?,choose =?,amount=?,size_=?,price=? WHERE table_ = ? and type=? and choose=?"
            _table_ = get_table_number()
            _type_ = request.form.get("sel1")
            _choose_ = request.form.get("sel2")
            _amount_ = request.form["amount"]
            _size_ = request.form["size"]
            _price_ = get_price(_type_, _amount_, _size_, _choose_)
            conn = sqlite3.connect('database.db')
            _get_message_update_(_table_, _type_, _choose_)
            cursor = conn.cursor()
            cursor.execute(update, (_table_, _type_, _choose_, _amount_, _size_, _price_, table, type, choose,))
            conn.commit()
            return redirect('/Take_order')

        elif request.form.get("confirm"):
            _reset_message_()
            conn = sqlite3.connect('database.db')
            table = get_table_number()
            table_nodes = "SELECT table_nodes FROM Nodes WHERE table_=?"
            table_node = conn.execute(table_nodes, (table,))
            result = table_node.fetchone()
            if result == None:
                cursor = conn.cursor()
                delete = "DELETE FROM Nodes WHERE table_nodes=? and table_=?"
                cursor.execute(delete, (0, table,))
            conn.commit()
            return Baristas()

    else:
        table = get_table_number()
        check = search_(table)
        if check == 1 or check == -1:
            __error__()
            conn = sqlite3.connect('database.db')
            headings = ("Table", "Order", "Amount", "Size", "Price", "Total")
            order = conn.execute("SELECT table_,table_nodes,flag,total FROM Nodes ORDER BY table_ ASC;")
            result = order.fetchall()
            table = conn.execute("SELECT choose,amount,size_,price FROM Take_order ORDER BY table_ ASC;")
            result1 = table.fetchall()
            return render_template('Baristas.html', headings=headings, data=zip(result1, result),
                                   message=_get__message_())
        else:
            table_num = get_table_number()
            headings = ("Type", "Order", "Amount", "Size", "Price")
            conn = sqlite3.connect('database.db')
            table = "SELECT type,choose,amount,size_,price FROM Take_order WHERE table_ = ?"
            table = conn.execute(table, (table_num,))
            result = table.fetchall()
            table1 = conn.execute("SELECT name FROM Hot_Drinks;")
            result1 = table1.fetchall()
            table2 = conn.execute("SELECT name FROM Soft_Drinks;")
            result2 = table2.fetchall()
            table3 = conn.execute("SELECT name FROM Meals;")
            result3 = table3.fetchall()
            table4 = conn.execute("SELECT name FROM Snacks;")
            result4 = table4.fetchall()
            total_()
            return render_template('Baristas-Order.html', headings=headings, data=result, data1=result1, data2=result2,
                                   data3=result3, data4=result4, message=_get__message_())


def __flag__(num):
    global flag__
    flag__ = num


def get__flag__():
    global flag__
    return flag__


def total_():
    conn = sqlite3.connect('database.db')
    table = conn.execute("SELECT num FROM seats ORDER BY num ASC;")
    result = table.fetchall()
    for x in result:
        table_ = "SELECT SUM(price) FROM Take_order WHERE table_=?"
        result_ = conn.execute(table_, (int(x[0]),)).fetchone()
        table__ = "SELECT vip FROM seats WHERE num=?"
        result__ = conn.execute(table__, (int(x[0]),)).fetchone()
        vip = "SELECT sale FROM Vip WHERE vip=?"
        result___ = conn.execute(vip, ('Yes',)).fetchone()
        if result_ != (None,):
            if result__ == ('No',):
                z = """UPDATE Nodes SET total = ? WHERE table_ = ?"""
                conn.execute(z, (int(result_[0]), int(x[0])))
            elif result__ == ('Yes',):
                z = """UPDATE Nodes SET total = ? WHERE table_ = ?"""
                conn.execute(z, (int(result_[0]) - (int(result_[0]) * int(result___[0])) / 100, int(x[0])))
    conn.commit()


def get_id():
    global id
    conn = sqlite3.connect('database.db')
    id_ = "SELECT MAX(id) FROM Nodes WHERE table_=?"
    result = conn.execute(id_, (get_table_number(),)).fetchone()
    return result[0]


def flag__():
    global flag_
    return flag_


def get_flag_(num):
    global flag_
    flag_ = num


def _id_():
    global id
    id = id + 1
    return id


def get_flag():
    global flag
    return flag


def flag_(flag__):
    global flag
    flag = flag__


def get_table_number():
    global table_number
    return table_number


def __error__():
    global _message_
    _message_ = "Invalid input"


def success():
    global _message_
    _message_ = "Success"


def _reset_message_():
    global _message_
    _message_ = ''


def _get__message_():
    global _message_
    return _message_


def _get_message_delete_(table, type, choose, amount, size):
    global _message_
    flag = 1
    temp = 1
    L = 1
    V = 1
    g = 1
    conn = sqlite3.connect('database.db')

    table_ = conn.execute("SELECT table_ FROM Take_order;")
    result = table_.fetchall()
    for row in result:
        if str(row[0]) == table:
            flag = 0
            break
        else:
            flag = 1

    type_ = conn.execute("SELECT type FROM Take_order;")
    result = type_.fetchall()
    for row in result:
        if row == (type,):
            temp = 0
            break
        else:
            temp = 1

    choose_ = conn.execute("SELECT choose FROM Take_order;")
    result = choose_.fetchall()
    for row in result:
        if row == (choose,):
            L = 0
            break
        else:
            L = 1

    amount_ = conn.execute("SELECT amount FROM Take_order;")
    result = amount_.fetchall()
    for row in result:
        if str(row[0]) == amount:
            V = 0
            break
        else:
            V = 1

    size_ = conn.execute("SELECT size_ FROM Take_order;")
    result = size_.fetchall()
    for row in result:
        if row == (size,):
            g = 0
            break
        else:
            g = 1

    if temp == 0 and flag == 0 and L == 0 and V == 0 and g == 0:
        _message_ = ''
        return 0
    else:
        _message_ = "Invalid input"
        return 1


def _get_message_update_(table, type, choose):
    global _message_
    flag = 1
    temp = 1
    L = 1
    conn = sqlite3.connect('database.db')

    table_ = conn.execute("SELECT table_ FROM Take_order;")
    result = table_.fetchall()
    for row in result:
        if str(row[0]) == table:
            flag = 0
            break
        else:
            flag = 1

    type_ = conn.execute("SELECT type FROM Take_order;")
    result = type_.fetchall()
    for row in result:
        if row == (type,):
            temp = 0
            break
        else:
            temp = 1

    choose_ = conn.execute("SELECT choose FROM Take_order;")
    result = choose_.fetchall()
    for row in result:
        if row == (choose,):
            L = 0
            break
        else:
            L = 1

    if temp == 0 and flag == 0 and L == 0:
        _message_ = ''
    else:
        _message_ = "Invalid input"


def get_price(type, amount, size, choose):
    conn = sqlite3.connect('database.db')
    if type == "Hot_Drinks":
        price_search_s = "SELECT price_s FROM Hot_Drinks WHERE name = ?"
        price_search_m = "SELECT price_m FROM Hot_Drinks WHERE name = ?"
        price_search_l = "SELECT price_l FROM Hot_Drinks WHERE name = ?"
        price_s = conn.execute(price_search_s, (choose,))
        price_m = conn.execute(price_search_m, (choose,))
        price_l = conn.execute(price_search_l, (choose,))
        price_s_ = price_s.fetchone()[0]
        price_m_ = price_m.fetchone()[0]
        price_l_ = price_l.fetchone()[0]
        if size == 'M':
            return int(price_m_) * int(amount)
        elif size == 'L':
            return int(price_l_) * int(amount)
        else:
            return int(price_s_) * int(amount)

    if type == "Soft_Drinks":
        price_search_s = "SELECT price_s FROM Soft_Drinks WHERE name = ?"
        price_search_m = "SELECT price_m FROM Soft_Drinks WHERE name = ?"
        price_search_l = "SELECT price_l FROM Soft_Drinks WHERE name = ?"
        price_s = conn.execute(price_search_s, (choose,))
        price_m = conn.execute(price_search_m, (choose,))
        price_l = conn.execute(price_search_l, (choose,))
        price_s_ = price_s.fetchone()[0]
        price_m_ = price_m.fetchone()[0]
        price_l_ = price_l.fetchone()[0]
        if size == 'M':
            return int(price_m_) * int(amount)
        elif size == 'L':
            return int(price_l_) * int(amount)
        else:
            return int(price_s_) * int(amount)

    if type == "Meals":
        price_search_s = "SELECT price_s FROM Meals WHERE name = ?"
        price_search_m = "SELECT price_m FROM Meals WHERE name = ?"
        price_search_l = "SELECT price_l FROM Meals WHERE name = ?"
        price_s = conn.execute(price_search_s, (choose,))
        price_m = conn.execute(price_search_m, (choose,))
        price_l = conn.execute(price_search_l, (choose,))
        price_s_ = price_s.fetchone()[0]
        price_m_ = price_m.fetchone()[0]
        price_l_ = price_l.fetchone()[0]
        if size == 'M':
            return int(price_m_) * int(amount)
        elif size == 'L':
            return int(price_l_) * int(amount)
        else:
            return int(price_s_) * int(amount)

    if type == "Snacks":
        price_search_s = "SELECT price_s FROM Snacks WHERE name = ?"
        price_search_m = "SELECT price_m FROM Snacks WHERE name = ?"
        price_search_l = "SELECT price_l FROM Snacks WHERE name = ?"
        price_s = conn.execute(price_search_s, (choose,))
        price_m = conn.execute(price_search_m, (choose,))
        price_l = conn.execute(price_search_l, (choose,))
        price_s_ = price_s.fetchone()[0]
        price_m_ = price_m.fetchone()[0]
        price_l_ = price_l.fetchone()[0]
        if size == 'M':
            return int(price_m_) * int(amount)
        elif size == 'L':
            return int(price_l_) * int(amount)
        else:
            return int(price_s_) * int(amount)


def search_(num):
    helper = 1
    conn = sqlite3.connect('database.db')
    if num != '':
        num_table = conn.execute("SELECT num FROM seats;")
        result = num_table.fetchall()
        for row in result:
            if row == (int(num),):
                helper = 0
                break
            else:
                helper = 1

        return helper
    else:
        return -1


def check_table():
    conn = sqlite3.connect('database.db')
    x = "SELECT table_ FROM Take_order"
    x_ = conn.execute(x)
    for row in x_:
        if row == (int(get_table_number()),):
            return 1
            break
    return 0


def check_table_():
    conn = sqlite3.connect('database.db')
    x = "SELECT table_ FROM Total"
    x_ = conn.execute(x)
    for row in x_:
        if row == (int(get_table_number()),):
            return 1
            break
    return 0


if __name__ == "__main__":
    app.run(debug=True)
