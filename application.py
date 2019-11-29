import requests
from flask import Flask, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from extra import login_required
import pymysql

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:210377091ztc@localhost:3306/attempt?charset=utf8mb4'
db = SQLAlchemy(app)

conn = pymysql.connect(host='localhost', port=3306,  user='root', passwd='210377091ztc', db="attempt")
cur = conn.cursor()

# 登录
@app.route("/login")
def get_token():
    username = request.args.get('username')
    password = request.args.get('password')

    url = 'https://os.ncuos.com/api/user/token'

    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "username": username,
        "password": password
    }
    r = requests.post(url, headers=headers, json=body)
    if username and password:
        session['username'] = username
        session['password'] = password

    return r.json()

# 退出登录
@app.route('/logout', methods=["GET"])
def logout():
    session.clear()  # 删除所有session
    return redirect(url_for('get_token'))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    text = db.relationship('Note', backref='user')

    def __repr__(self):
        return '<User {}> '.format(self.name)

class Note(db.Model):
    __tablename__ = 'texts'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), nullable=False)
    time = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Note {}> '.format(self.user_text)


# 创建用户名
@app.route('/create')
@login_required
def create_user():
    input_name = request.args.get('name')
    name_ = User(name=input_name)

    db.session.add_all([name_])
    db.session.commit()

# 添加手账
@app.route('/notepad/add')
# @login_required
def add_notepad():
    text = request.args.get('text')
    time = request.args.get('time')
    if not text or not time:
        return 'please request with text and time args'
    new_note = Note(text=text, time=time)
    db.session.add_all([new_note])
    db.session.commit()
    return text, time

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
