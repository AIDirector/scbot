from .Employees import EmployeesTable
from .EmployeeTypes import EmployeeTypesTable


def init():
    therapist = EmployeeTypesTable.create(type_name="therapist", display_name="Терапевт")
    otolaryngologist = EmployeeTypesTable.create(type_name="otolaryngologist", display_name="Лор")
    neurologist = EmployeeTypesTable.create(type_name="neurologist", display_name="Невролог")

    EmployeesTable.create(name="Трофимов Антон Рубенович", type=therapist, photo_filename="doctor1.jpg")
    EmployeesTable.create(name="Степанов Герман Павлович", type=therapist, photo_filename="doctor2.jpg")
    EmployeesTable.create(name="Ефимова Алира Глебовна", type=otolaryngologist, photo_filename="doctor3.jpg")
    EmployeesTable.create(name="Фокина Роза Куприяновна", type=neurologist, photo_filename="doctor4.jpg")
