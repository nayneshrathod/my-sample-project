import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
from yaml import load, dump

app = Flask(__name__)
Bootstrap(app)

db = yaml.load(open('db.yaml'))
# app.config['MYSQL_']
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = os.urandom(24)
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    # users = ''
    if request.method == 'POST':
        try:
            form = request.form
            fname = form['first_name']
            lname = form['last_name']
            gender = form['gender']
            address = form['address']
            mobile = form['mobile']
            email = form['email']
            username = form['username']
            password = form['password']
            cur = mysql.connection.cursor()
            password = generate_password_hash(password)
            cur.execute("INSERT INTO sample_user(fname,lname,address,gender,mobile,email,username,password)"
                        " values(%s,%s,%s,%s,%s,%s,%s,%s)",
                        (fname, lname, address, gender, mobile, email, username, password))
            mysql.connection.commit()
            flash("Successfully Inserted Data", 'success')
            # get_flash
            # mysql.connection.close()
            # users = 'my naynesh'
            cur = mysql.connection.cursor()
            res_val = cur.execute("SELECT * from sample_user")
            if res_val > 0:
                users = cur.fetchall()
                # session['username'] = users[0]['username']
                # session['password'] = str(check_password_hash(users[0]['password'], 'MyMom@000'))


            else:
                users = 'cur.fetchall()'
                # return render_template('index.html')
            # return 'succsess'
            # return redirect(index)
            # return "Good"
            # fruits = ['Apple' ,'Orange']
            return render_template('index.html', users=users, active="active")
        except:
            flash("failed To Inserted Data", 'danger')

    if request.method == 'GET':
        cur = mysql.connection.cursor()

        # cur.execute("INSERT INTO user Values(%s)", [ 'Swati'])
        # mysql.connection.commit()
        res_val = cur.execute("SELECT * from sample_user")
        if res_val > 0:
            users = cur.fetchall()
            session['username'] = users[0]['username']

        else:
            # users = 'cur.fetchall()'
            return render_template('index.html')
        # return 'succsess'
        # users = list(users)
        # print(users )
        # print(users[0])
        return render_template('index.html', users=users, active="active")
    return render_template('index.html', active="active")

    # return "Hello World.!"
    # return render_template('index.html',frut = fruits)
    # return redirect(url_for('about'))


@app.route('/about')
def about():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        res_val = cur.execute("SELECT * from sample_user")
        if res_val > 0:
            users = cur.fetchall()
        else:
            return render_template('about.html', active="active")
    return render_template('about.html', users=users, active="active")


@app.route('/css')
def css():
    return render_template('css.html', active="active")


@app.errorhandler(404)
def page_not_found(e):
    return "render_template('css.html')"


if __name__ == '__main__':
    app.run(debug=True, port=5100)
