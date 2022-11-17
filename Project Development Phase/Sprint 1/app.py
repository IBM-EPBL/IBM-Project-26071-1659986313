import re
import ibm_db
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=rgd26397;PWD=G2CL8D9vsH6noeUp", '', '')
print(conn)
print("Connecting Successful............")


@app.route('/')
def homer():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    # global userid
    # msg = ''
    if request.method == "GET":
        return render_template("login.html");
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =? AND password =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid = account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
            return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():

    msg = ''
    if request.method == 'GET':
        msg = 'Please fill out the form !'
        return render_template('Register.html', msg=msg)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # print(username, email, password)
        
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        
        if account:
            msg = 'Account already exists !'
            print('s')
            return msg 
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
            print("f")
            return msg
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers!'
            print(msg)
            return msg
        else:
            insert_sql = "INSERT INTO users VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return msg
    


@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')
# sendmail(TEXT,"sandeep@thesmartbridge.com")
# sendgridmail("sandeep@thesmartbridge.com",TEXT)


@app.route('/display')
def display():
    print(session["username"], session['id'])
    cursor = conn.connection.cursor()
    cursor.execute('SELECT * FROM job WHERE userid = % s',
                   (session['id'],))
    account = cursor.fetchone()
    print("accountdislay", account)
    return render_template('display.html', account=account)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
