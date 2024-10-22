from flask import Flask, render_template, request, redirect, url_for, flash, session  
from flask_sqlalchemy import SQLAlchemy  
from werkzeug.security import generate_password_hash, check_password_hash  
import sqlite3  
  
app = Flask(__name__)  
app.secret_key = 'your_secret_key'  # 用于会话管理，请替换为更安全的密钥  
app.config['SESSION_COOKIE_HTTPONLY'] = True  
app.config['SESSION_PROTECTION'] = 'strong'  
  
# 使用SQLite数据库  
# 这里为了简单起见，直接使用sqlite3库  
# 如果你想使用Flask-SQLAlchemy，可以注释掉下面的代码，并取消注释下面的Flask-SQLAlchemy部分  
  
def init_db():  
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()  
    cursor.execute('''  
    CREATE TABLE IF NOT EXISTS users (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        username TEXT NOT NULL UNIQUE,  
        password TEXT NOT NULL  
    )  
    ''')  
    conn.commit()  
    conn.close()  
  
# @app.before_first_request  
# def create_tables():  
#     init_db()  
  
@app.route('/')  
def index():  
    return redirect(url_for('login'))  
  
@app.route('/login', methods=['GET', 'POST'])  
def login():  
    if request.method == 'POST':  
        username = request.form['username']  
        password = request.form['password']  
          
        conn = sqlite3.connect('database.db')  
        cursor = conn.cursor()  
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))  
        user = cursor.fetchone()  
          
        if user and check_password_hash(user[2], password):  
            session['username'] = user[1]  
            return redirect(url_for('welcome'))  
        else:  
            flash('Invalid username or password')  
            return redirect(url_for('login'))  
      
    return render_template('login.html')  
  
@app.route('/welcome')  
def welcome():  
    if 'username' in session:  
        return f'Welcome, {session["username"]}!'  
    return redirect(url_for('login'))  
  
@app.route('/logout')  
def logout():  
    session.pop('username', None)  
    return redirect(url_for('login'))  
  
if __name__ == '__main__':  
    app.run(debug=True)