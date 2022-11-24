from peewee import PrimaryKeyField, TextField, IntegerField

from . import BaseModel


class UsersTable(BaseModel):
    user_id = PrimaryKeyField(null=False)
    user_name = TextField(null=False)
    telegram_id = IntegerField(unique=True)
    phone_number = TextField()
    email = TextField()
    medical_policy = IntegerField()

    @staticmethod
    def from_telegram_id(tg_id):
        return UsersTable.get(UsersTable.telegram_id == tg_id)

    @staticmethod
    def delete_user_by_telegram_id(tg_id):
        UsersTable.delete().where(UsersTable.telegram_id == tg_id).execute()
