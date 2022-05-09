import telebot
from telebot import types
from dbhelper import DBHelper
import sqlite3

bot = telebot.TeleBot('5316835653:AAF7HRhti7HTxpCMEUGaFrVHdhQfaTK-iyE')

db = DBHelper()
user_data = {}


class Users:
    name: str
    surname: str
    phone: str
    classes: str

    def __init__(self, name, surname, phone, classes):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.classes = classes

        db.db_table_name(name, surname, phone, classes)


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Понедельник")
    item2 = types.KeyboardButton("Вторник")
    item3 = types.KeyboardButton("Среда")
    item4 = types.KeyboardButton("Четверг")
    item5 = types.KeyboardButton("Пятница")
    item6 = types.KeyboardButton("Суббота")
    item7 = types.KeyboardButton("База занятий 🔈")
    item8 = types.KeyboardButton("👋Добавить гостя \n для совместных занятий")

    markup.add(item1, item2, item3, item4, item5, item6, item7, item8)

    bot.send_message(message.chat.id,
                     "Hi, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот-Дневник занятий VL, присоединяйтесь!!!".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
# @bot.message_handler(func=lambda message: db.db_table_val(user_id = message.from_user.id, user_name = message.from_user.first_name, user_surname = message.from_user.last_name, username = message.from_user.username))
# def lalala(message):
def lalala(message, db=DBHelper()):
    text = message.text.lower()
    print(text)
    if text in ['привет', 'hi', 'hello']:
        bot.send_message(message.chat.id, ' 🙂 Привет! Ваше имя добавлено в базу данных!')

        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_surname = message.from_user.last_name
        username = message.from_user.username

        db.db_table_val(us_id, us_name, us_surname, username)


    elif message.chat.type == 'private':
        if message.text == 'Понедельник':
            bot.send_message(message.chat.id, 'Пилатес Bok 🏃‍')
        if message.text == 'Вторник':
            bot.send_message(message.chat.id, 'Курсы BelHard 💻')
        if message.text == 'Среда':
            bot.send_message(message.chat.id, u'Пилатес Bok 🏃‍\n Клуб Book club 📗')
        if message.text == 'Четверг':
            bot.send_message(message.chat.id, 'Курсы Belhard 💻')
        if message.text == 'Пятница':
            bot.send_message(message.chat.id, 'Сoffee with friends ☕')
        if message.text == 'Суббота':
            bot.send_message(message.chat.id, 'Сountry house 🏠')
        if message.text == 'База занятий 🔈':
            bot.send_message(message.chat.id,
                             u'понедельник и среда Пилатес Bok 📇\n вторник и четверг Belhard 📉\n среда Клуб Book club 💻\n пятница Кофе ☕\n суббота и воскресенье Сountry house 🔨')
        elif message.text == '👋Добавить гостя \n для совместных занятий':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Автоматически добавить в базу данных", callback_data='good')
            item21 = types.InlineKeyboardButton("Добавиться самостоятельно", callback_data='bad')
            item22 = types.InlineKeyboardButton("❓Вывести список зарегистрировавшихся", callback_data='classes')
            item23 = types.InlineKeyboardButton("Вывести список по занятию", callback_data='chat_id')
            item3 = types.InlineKeyboardButton("Выход", callback_data='exit')
            markup.add(item1, item21, item22, item23, item3)
            bot.send_message(message.chat.id, "Запишитесь в список для совместных занятий 💪💪", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Поприветствуйте бот для добавления в базу данных')
            elif call.data == 'bad':
                msg = bot.send_message(call.message.chat.id, 'Введите имя')
                bot.register_next_step_handler(msg, process_firstname_step)
            elif call.data == 'chat_id':
                msg = bot.send_message(call.message.chat.id, 'Введите занятие')
                bot.register_next_step_handler(msg, handler_chat)
                # bot.send_message(msg, text)
                # bot.send_message(chat_id, text)
                # bot.message_handler(msg, process_classes_step)
            elif call.data == 'classes':
                print("classes")
                itemst = db.get_items()
                print(itemst)
                if len(itemst) > 0:
                    for j in itemst:
                        s = ''
                        for k in j:
                            s = s + '  👉   ' + k
                        s = s + '    '
                        bot.send_message(call.message.chat.id, s)
                        print(j)

            elif call.data == 'correct_classes':
                print("=============")
                msg = bot.send_message(call.message.chat.id, 'Введите класс')
                #user_id = call.message.from_user.id
                # user_id = msg.from_user.id
                # Users.classes = call.message.text
                # Users.classes = msg.text
                # classes = db.get_classes_inf(Users.classes)
                # bot.send_message(id(classes), "Принято")
                # print("correct_classes")
                # itm = db.get_classes_inf(Users.classes)
                # print(Users.classes)
                # print(itm)
                #if itm == str.lower(classes):
                # if len(itm) > 0:
                #     for q in itm:
                #         s = ' '
                #         for k in q:
                #             s = s + ' + ' + k
                #         s = s + ' + '
                #         bot.send_message(call.message.chat.id, s)
                #         print(q)

            else:
                bot.edit_message_text("выход", call.message.chat.id, call.message.message_id, reply_markup=None)

    except:
        pass


def send_welcome(message):
    msg = bot.send_message(message.chat.id, "Введите имя 👦")
    bot.register_next_step_handler(msg, process_firstname_step)


def process_firstname_step(message):
    try:
        Users.name = message.text
        msg = bot.send_message(message.chat.id, "Фамилию:")
        bot.register_next_step_handler(msg, process_lastname_step)
    except Exception as e:
        bot.reply_to(message, "Ошибка ввода имени")


def process_lastname_step(message):
    try:
        Users.surname = message.text
        print(Users.surname)
        msg = bot.send_message(message.chat.id, "Телефон:")
        bot.register_next_step_handler(msg, process_phone_step)
    except Exception as e:
        bot.reply_to(message, "Ошибка ввода фамилии")


def process_phone_step(message):
    try:
        user_id = message.from_user.id
        print(user_id)
        Users.phone = message.text
        print(Users.phone)
        # db.db_table_name(user_id, Users.name, Users.surname, Users.phone )
        msg = bot.send_message(message.chat.id, "Занятие:")
        bot.register_next_step_handler(msg, process_classes_step)
    except Exception as e:
        bot.reply_to(message, "Ошибка ввода телефона")


def process_classes_step(message):
    try:
        user_id = message.from_user.id
        print(user_id)
        Users.classes = message.text
        print(Users.classes)
        db.db_table_name(user_id, Users.name, Users.surname, Users.phone, Users.classes)
        bot.send_message(user_id, "Вы успешно зарегистрированы")
    except Exception as e:
        bot.reply_to(message, "Ошибка ввода занятия")

# def process_classes_step(message):
#     try:
#         user_id = message.from_user.id
#         Users.classes = message.text
#         db.get_classes_inf(Users.classes)
#         bot.send_message(user_id, "Принято")
#     except Exception as e:
#         bot.reply_to(message, "Ошибка класса")


@bot.message_handler(content_types=['text'])
def handler_chat(message):
            user_id = message.from_user.id
            Users.classes = message.text
            print(message.text)
            exists = db.get_classes_inf(Users.classes)
            print(exists)
            text = "Записан" if exists else "Не записан"
            bot.send_message(user_id, text)
            #if exists == True:
            if exists == [1]:
                print("Да")
                data2 = db.get_all_classes(Users.classes)
                print(data2)
                chat_id = message.chat.id
                bot.send_message(chat_id, '\n'.join(map(str, data2)))


# RUN
# bot.polling(none_stop=True)

def main():
    bot.polling(none_stop=True)
    db.setup()


if __name__ == '__main__':
    main()
