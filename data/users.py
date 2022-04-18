import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    inst = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    vk = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    vk_friends = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    vk_photos = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    telegram = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tasks = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    scores = sqlalchemy.Column(sqlalchemy.REAL, nullable=True, default=0)
    progress = sqlalchemy.Column(sqlalchemy.INT, nullable=True, default=0)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    telegram_flag = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='')
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)