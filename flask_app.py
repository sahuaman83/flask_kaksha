from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import yaml
import json

app = Flask(__name__)

# app.secret_key = 'your secret key'

# Configure db using yaml configuration file
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        password = userDetails['pass']
            # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM USER WHERE name = %s AND password = %s', (name, password))
            # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            # session['loggedin'] = True
            # session['user_id'] = account['user_id']
            # session['name'] = account['name']

            # Redirect to page with items from the wishlist which has a discount greater than “30%”
            return redirect('/items')
        else:
            # Account doesn't exist or name/password incorrect
            return 'Incorrect username/password!'
    return render_template('index.html')

@app.route('/items')
def users():
    return render_template('home.html')

@app.route('/discount')
def discount():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM ITEM i INNER JOIN WISHLIST w ON w.item_id=i.item_id INNER JOIN USER u ON w.user_id=u.user_id WHERE i.discount>30')
    items = cursor.fetchall()
    return render_template('items.html',items=items)

@app.route('/itemdetail')
def itemdetail():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM ITEM WHERE item_category="Books" and details="Prof JK Chhabra"')
    itemdetail = cursor.fetchall()
    return render_template('itemdetail.html',itemdetail=itemdetail)

@app.route('/rated')
def rated():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM ITEM WHERE rating<=5 ORDER BY rating ASC')
    rated = cursor.fetchall()
    return render_template('rated.html',rated=rated)


@app.route('/notification')
def notification():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT user_id,contact FROM USER')
    row_headers=[x[0] for x in cursor.description]
    notification = cursor.fetchall()
    json_data=[]
    for result in notification:
        json_data.append(dict(zip(row_headers,result)))

    cursor.execute('SELECT * FROM ITEM WHERE rating<=5  and item_category="Books" and details="Prof JK Chhabra"')
    row_headers=[x[0] for x in cursor.description]
    notification = cursor.fetchall()
    for result in notification:
        json_data.append(dict(zip(row_headers,result)))

    return json.dumps(json_data)

    
if __name__ == '__main__':
    app.run(debug=True)