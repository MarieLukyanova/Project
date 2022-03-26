import datetime

from flask import Flask
from flask import render_template, redirect, request, make_response, session, abort
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm, EditForm
from flask_login import LoginManager, login_required, current_user

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
def profile():
    return render_template('Profile.html')

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
        user = User(
            name=form.name.data,
            email=form.email.data,
            inst=form.inst.data,
            vk=form.vk.data,
            tasks=0,
            about=''
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/profile')
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
            return redirect("/profile")
        return render_template('Авторизация.html', title='Авторизация', email=request.form['email'],
                               password=request.form['password'], submit=request.form['submit'],
                               message="Неправильный логин или пароль", form=form)
    return render_template('Авторизация.html', title='Авторизация', form=form)

@app.route('/pofileedit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_pofile(id):
    form = EditForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        if user:
            form.name.data = user.name
            form.email.data = user.email
            form.tel.data = user.tel
            form.inst.data = user.inst
            form.vk.data = user.vk
            form.about.data = user.about
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        if user:
            form.name.data = user.name
            form.email.data = user.email
            form.tel.data = user.tel
            form.inst.data = user.inst
            form.vk.data = user.vk
            form.about.data = user.about
            db_sess.commit()
            return redirect('/profile')
        else:
            abort(404)
    return render_template('',
                           title='Редактирование профиля',
                           form=form)


def main():
    db_session.global_init('db/life_of_party.sqlite')
    app.run()


if __name__ == '__main__':
    main()