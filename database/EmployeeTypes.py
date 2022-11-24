from peewee import PrimaryKeyField, TextField, IntegerField

from . import BaseModel


class EmployeeTypesTable(BaseModel):
    employee_types_id = PrimaryKeyField(null=False)
    type_name = TextField(unique=True, null=False)
    display_name = TextField(null=True)
