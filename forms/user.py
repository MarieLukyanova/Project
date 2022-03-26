# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, TextAreaField


class RegisterForm(FlaskForm):
    name = StringField('Ваше имя')
    email = EmailField('Почта')
    password = PasswordField('Пароль')
    password_again = PasswordField('Повторите пароль')
    tel = StringField('Телефон')
    inst = StringField('Instagram')
    vk = StringField('Вконтакте')
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта')
    password = PasswordField('Пароль')
    submit = SubmitField('Войти')


class EditForm(FlaskForm):
    name = StringField('Ваше имя')
    email = EmailField('Почта')
    tel = StringField('Телефон')
    inst = StringField('Instagram')
    vk = StringField('Вконтакте')
    about = TextAreaField('Немного о себе')
    submit = SubmitField('Войти')