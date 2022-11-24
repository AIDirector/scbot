class Messages:
    def __init__(self, messages: dict[str, str]):
        self.messages: dict[str, str] = messages

    def get_message(self, message_name, *args, **kwargs):
        if message_name in self.messages:
            return self.messages[message_name].format(*args, **kwargs)


messages_dict = {
    "hello": "Здравствуйте!",
    'registered': "Вы уже зарегестрированы! Войдите или удалите аккаунт. "
                  "Внимание, при удалении аккаунта все ваши записи отменятся!",
    "intro": "Это бот для записи на приём! Тут вы можете записаться.",
    "registration_start": "Прошу пройти регистрацию. Пожалуйста, введите полис",
    "registration_medical_policy_ok": "Полис принят",
    "registration_medical_policy_failed": "Кажется, вы ошиблись. Введите, пожлауйста, полис заново",
    "registration_get_phone": "Пожалуйста, введите номер телефона",
    "registration_phone_ok": "Телефон принят",
    "registration_phone_failed": "Кажется, вы ошиблись. Введите, пожлауйста, телефон заново",
    "registration_get_email": "Пожалуйста, введите email",
    "registration_email_ok": "Email принят",
    "registration_email_failed": "Кажется, вы ошиблись. Введите, пожлауйста, email заново",
    "not_understand": "Я вас не понимаю",
    "book_employee_start": "Вы записываетесь к {employee_name}. Выберите день посещения!",
    "book_employee_day_ok": "Теперь выберите время",
    "book_employee_day_fail": "День не распознан",
    "book_employee_time_fail": "Время не распознано",
    "book_data_request_accept": "Подтвердите запись!\n{employee_name}\n{book_day} {book_time}",
    "book_data_ok": "Вы успешно записаны!",
    "cancel_book_employee": "Запись отменена",

}


messages = Messages(messages_dict
                    )
