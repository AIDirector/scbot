from peewee import PrimaryKeyField, TextField, IntegerField, ForeignKeyField

from . import BaseModel, UsersTable, EmployeesTable


class BooksTable(BaseModel):
    book_id = PrimaryKeyField(null=False)
    user = ForeignKeyField(UsersTable, backref="book_user_id")
    employee = ForeignKeyField(EmployeesTable, backref="book_employee_id")
    day = TextField(null=False)
    time = TextField(null=False)

    @staticmethod
    def books_by_user(user):
        return BooksTable.select().where(BooksTable.user == user).execute()

    @staticmethod
    def books_by_user_telegram_id(tg_id):
        return BooksTable.select().join(UsersTable).where(UsersTable.telegram_id == tg_id).execute()
