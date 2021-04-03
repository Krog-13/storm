from flask_sqlalchemy import SQLAlchemy
import os
from api import send_weather, city
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, redirect, request, flash, url_for, abort
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
from UserLogin import UserLogin

#SECRET_KEY = os.urandom()
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f"<users {self.id}>"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_city = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(200))
    url = db.Column(db.String(50))

    def __repr__(self):
        return f"<city {self.name_city}>"


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, Users)

@app.route("/")
def index():
    info = 'Goust'
    city = []
    try:
        city = City.query.all()
    except:
        print('error db')
    finally:
        if current_user.is_authenticated:
            info = current_user.getEmail()
    return render_template("index.html", title="Main", list=info, city=city)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            hash = generate_password_hash(form.psw.data)
            u = Users(email=form.email.data, psw=hash)
            if u:
                print(u, 'ererereww')
                db.session.add(u)
                db.session.flush()

            p = Profiles(name=form.name.data, old=form.old.data,
                         city=form.city.data, user_id=u.id)
            if p:
                print(p, 'ererere')
                db.session.add(p)
                db.session.commit()
                flash("success", "success")
        except:
            flash("Error DB", "success")
            db.session.rollback()
            print('error db fuck')

    return render_template('register.html', title='Register', form=form)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.psw, form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("index"))
        flash("Неверная пара логин/пароль", "error")

    return render_template('login.html', title='Login', form=form)

@app.route('/weather')
@login_required
def weather():
    weather = send_weather(5, 'Astana')
    return render_template("weather.html", title="Профиль", weather=weather)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))

@app.route("/post/<alias>")
@login_required
def showPost(alias):
    town = City.query.filter_by(url=alias).first_or_404()
    weather = send_weather(2, town.name_city)

    return render_template('weather.html', weather=weather, town=town)

if __name__ == "__main__":
    print('start')
    app.run(debug=False)