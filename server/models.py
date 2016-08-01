from peewee import (SqliteDatabase, TextField, Model)

db = SqliteDatabase('exotic.db')


class BaseModel(Model):

    class Meta:
        database = db


class User(BaseModel):
    email = TextField(unique=True)
    password = TextField()


class Rpi(BaseModel):
    name = TextField(unique=True)
    auth_key = TextField()


class Admin(BaseModel):
    name = TextField(unique=True)
    password = TextField()


db.connect()
db.create_tables([User, Rpi, Admin], safe=True)
