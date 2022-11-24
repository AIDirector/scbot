from peewee import SqliteDatabase, Model

database = SqliteDatabase('db.sqlite')


class BaseModel(Model):
    class Meta:
        database = database
