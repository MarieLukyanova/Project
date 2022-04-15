# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, TextAreaField, URLField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class RegisterForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    inst = StringField('Instagram', validators=[DataRequired()])
    vk = StringField('Вконтакте\n(короткое имя или id)', validators=[DataRequired()])
    telegram = StringField('Telegram', validators=[DataRequired()])
    submit = SubmitField('ЗАРЕГИСТРИРОВАТЬСЯ', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('ВОЙТИ', validators=[DataRequired()])


class EditForm(FlaskForm):
    name = StringField('Ваше имя')
    email = EmailField('Почта')
    inst = StringField('Instagram')
    vk = StringField('Вконтакте')
    telegram = StringField('Telegram')
    about = TextAreaField('Немного о себе')
    submit = SubmitField('Принять изменения')
