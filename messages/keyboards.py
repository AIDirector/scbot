from aiogram.types import ReplyKeyboardMarkup


class Keyboards:
    def __init__(self, keyboards: dict[str, str]):
        self.keyboards: dict[str, str] = keyboards

    def get_keyboard(self, keyboard_name):
        if keyboard_name in self.keyboards:
            return self.keyboards[keyboard_name]


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .add('Список специалистов', 'Записаться на приём').add('Информация', 'Мои записи')

choose_day_keyboard = ReplyKeyboardMarkup() \
    .add("Понедельник", "Вторник", "Среда") \
    .add("Четверг", "Пятница", "Суббота") \
    .add("Отменить")

choose_time_keyboard = ReplyKeyboardMarkup()

for i in range(15):
    hours = 9
    minutes = i * 15
    hours += minutes // 60
    minutes %= 60
    choose_time_keyboard.insert(f"{hours}:{minutes}")
choose_time_keyboard.add("Отменить")

accept_keyboard = ReplyKeyboardMarkup().add("Принять", "Отменить")

keyboards_dict = {
    "main_keyboard": main_keyboard,
    "choose_day_keyboard": choose_day_keyboard,
    "choose_time_keyboard": choose_time_keyboard,
    "accept_keyboard": accept_keyboard,
}

keyboards = Keyboards(keyboards_dict)
