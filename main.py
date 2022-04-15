import datetime
import os

from flask import Flask
from flask import render_template, redirect, request, make_response, session, abort
from data import db_session
from data.users import User
from data.vk import Friends, Photos, ID, Avatar, Name
from forms.user import RegisterForm, LoginForm, EditForm
from flask_login import LoginManager, login_required, current_user, \
    logout_user, login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template('Вступление.html')


@app.route("/profile")
@login_required
def profile():
    if current_user.progress == 0:
        percent = 100
    else:
        percent = current_user.progress
    if current_user.photo:
        photo = current_user.photo
    else:
        photo = 'https://acewebcontent.azureedge.net/GettyImages-542291608.jpg'
    return render_template('Profile.html', progress=percent, avatar=photo, vk_name=Name(current_user.vk))

@app.route("/info")
def info():
    return render_template('Информация.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('Регистрация.html', title='Регистрация', form=form, message='Пароль не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('Регистрация.html', title='Регистрация', form=form,
                                   message='Этот пользователь уже зарегестрирован')
        id = form.vk.data
        if id.isdigit():
            id = int(id)
        else:
            id = ID(id)
        user = User(
            name=form.name.data,
            email=form.email.data,
            inst=form.inst.data,
            telegram=form.telegram.data,
            vk=id,
            vk_friends=Friends(id),
            vk_photos=Photos(id),
            photo=Avatar(id)
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('Регистрация.html', title='Регистрация', form=form)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    session.permanent = True
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/profile")
        return render_template('Авторизация.html', title='Авторизация', email=request.form['email'],
                               password=request.form['password'], submit=request.form['submit'],
                               message="Неправильный логин или пароль", form=form)
    return render_template('Авторизация.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/pofileedit', methods=['GET', 'POST'])
@login_required
def edit_pofile():
    form = EditForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        if user:
            form.name.data = user.name
            form.email.data = user.email
            form.telegram.data = user.telegram
            form.inst.data = user.inst
            form.vk.data = user.vk
            form.about.data = user.about
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        if user:
            user.name = form.name.data
            user.email = form.email.data
            user.telegram = form.telegram.data
            user.inst = form.inst.data
            user.vk = form.vk.data
            user.about = form.about.data
            db_sess.commit()
            return redirect('/profile')
        else:
            abort(404)
    return render_template('Редактирование.html',
                           title='Редактирование профиля',
                           form=form)


@app.route('/add_photo', methods=['POST', 'GET'])
def add_photo():
    if request.method == 'GET':
        return render_template('Add_photo.html')
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        if user:
            file = request.files['file']
            file.save(os.path.join(f"/data/users/{user.id}"))
            user.photo = f"/data/users/{user.id}"
            db_sess.commit()
        return redirect('/profile')


def main():
    db_session.global_init('db/life_of_party.sqlite')
    app.run()


if __name__ == '__main__':
    main()