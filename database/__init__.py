from .database import BaseModel, database
from .EmployeeTypes import EmployeeTypesTable
from .Employees import EmployeesTable
from .Users import UsersTable
from .Books import BooksTable
from .Files import FilesTable

UsersTable.create_table()
EmployeeTypesTable.create_table()
EmployeesTable.create_table()
BooksTable.create_table()
FilesTable.create_table()



