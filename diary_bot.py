import telebot
from telebot import types
from dbhelper import DBHelper
import re
from config import bottoken

bot = telebot.TeleBot(bottoken)

db = DBHelper()
user_data = {}


class Users:
    name: str
    surname: str
    phone: []
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
    item1 = types.KeyboardButton("🏃Пилатес Bok")
    item2 = types.KeyboardButton("💻Курсы BelHard")
    item3 = types.KeyboardButton("📗Клуб Book club")
    item4 = types.KeyboardButton("☘Баня")
    item5 = types.KeyboardButton("☕Кофe c друзьями")
    item6 = types.KeyboardButton("🏠Дача")
    item7 = types.KeyboardButton("База курсов и занятий по интересам🔈")
    item8 = types.KeyboardButton("👋Добавить друзей \n для совместных занятий")

    markup.add(item1, item2, item3, item4, item5, item6, item7, item8)

    bot.send_message(message.chat.id,
                     "Hi, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот-Дневник занятий VL, присоединяйтесь и записывайтесь для совместного времяпрепровождения ✌️🤩 !!!".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message, db=DBHelper()):
    text = message.text.lower()
    print(text)
    if text in ['привет', 'hi', 'hello', 'хай', 'здравствуйте']:
        bot.send_message(message.chat.id, ' 🙂 Привет! Ваше имя добавлено в базу данных, я вам отпишусь!')

        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_surname = message.from_user.last_name
        username = message.from_user.username

        db.db_table_val(us_id, us_name, us_surname, username)


    elif message.chat.type == 'private':
        if message.text == '🏃Пилатес Bok':
            bot.send_message(message.chat.id, 'Понедельник и среда в 19:00')
        if message.text == '💻Курсы BelHard':
            bot.send_message(message.chat.id, 'Вторник и четверг в 18:30')
        if message.text == '📗Клуб Book club':
            bot.send_message(message.chat.id, u'Каждую вторую среду месяца в 20:30')
        if message.text == '☘Баня':
            bot.send_message(message.chat.id, 'Последнее воскресенье месяца в 12:00')
        if message.text == '☕Кофe c друзьями':
            bot.send_message(message.chat.id, 'Пятница в 18:00')
        if message.text == '🏠Дача':
            bot.send_message(message.chat.id, 'Дача в субботу и воскресенье, время договорное')
        if message.text == 'База курсов и занятий по интересам🔈':
            bot.send_message(message.chat.id,
                             u'Курсы и интересы на май, присоединяйтесь! \n 🏃Пилатес понедельник и среда в 19:00 \n 💻 Курсы Belhard вторник и четверг в 18:30 \n 📗 Клуб Book club 2-я среда в 20:30 \n ☕Кофе пятница в 18:00 \n 🏠 Дача суббота и воскресенье время договорное (к тяжкому труду прилагаются шашлыки🍗🍖) \n ☘Баня в последнее воскресенье месяца в 12:00')
        elif message.text == '👋Добавить друзей \n для совместных занятий':
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Автовыгрузка данных из телеги", callback_data='good')
            item21 = types.InlineKeyboardButton("Запишитесь самостоятельно, укажите куда", callback_data='bad')
            item22 = types.InlineKeyboardButton("❓Вывести весь список, не понятно? Нажми ниже ⬇", callback_data='classes')
            item23 = types.InlineKeyboardButton("Этот список выведет все по интересам", callback_data='chat_id')
            item3 = types.InlineKeyboardButton("Выход", callback_data='exit')
            # if message.text == 'Выход':
            #     bot.send_message(message.chat.id, 'Всем спасибо, обязательно перезвоню!!!')
            markup.add(item1, item21, item22, item23, item3)
            bot.send_message(message.chat.id, "Запишитесь в список для совместных занятий 💪 \n  🔫 автоматически  ↙ ↘  ручками 🖐", reply_markup=markup)


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
            else:
                bot.edit_message_text("Всем спасибо, обязательно перезвоню!!!", call.message.chat.id, call.message.message_id, reply_markup=None)

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
    user_id = message.from_user.id
    while True:
        Users.phone = message.text
        if re.match(r'[0-9@#$%^&+=]{1,}', Users.phone):
           break
        else:
            bot.reply_to(message, "Ошибка ввода телефона")
            send_welcome(message)
            return

    msg = bot.send_message(message.chat.id, "Занятие:")
    bot.register_next_step_handler(msg, process_classes_step)


def process_classes_step(message):
    try:
        user_id = message.from_user.id
        print(user_id)

        Users.classes = message.text
        Users.name = str.lower(Users.name)
        Users.surname = str.lower(Users.surname)
        Users.phone = str(Users.phone)
        print(Users.phone)

        Users.classes = str.lower(Users.classes)

        print(Users.classes)
        db.db_table_name(user_id, Users.name, Users.surname, Users.phone, Users.classes)
        bot.send_message(user_id, "Вы успешно зарегистрированы")
    except Exception as ex:
        bot.reply_to(message, "Ошибка ввода занятия")

@bot.message_handler(content_types=['text'])
def handler_chat(message):
            user_id = message.from_user.id
            Users.classes = str.lower(message.text)
            print(str(message.text))
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
