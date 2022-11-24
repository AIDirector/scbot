from peewee import PrimaryKeyField, TextField, IntegerField, ForeignKeyField

from . import BaseModel
from .EmployeeTypes import EmployeeTypesTable


class EmployeesTable(BaseModel):
    employee_id = PrimaryKeyField(null=False)
    name = TextField(null=False)
    type = ForeignKeyField(EmployeeTypesTable, backref='employee_type')
    photo_filename = TextField()

    @staticmethod
    def all_employees():
        return EmployeesTable.select().order_by(EmployeesTable.type.asc()).execute()
