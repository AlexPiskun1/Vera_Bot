# vera_piskun_bot  Бот отвечает на часто задаваемые вопросы
import telebot
from telebot import types

import sqlite3
import re
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv("key_bot"))


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}, я телеграм бот,  жду Ваших команд")
    kb_main(message)

    db = sqlite3.connect("vera_piskun_server.db")
    sql = db.cursor()
    sql.execute(f"SELECT id FROM client WHERE id = '{message.from_user.id}'")
    if sql.fetchone() is None:
        sql.execute(
            f"INSERT INTO client (id,user_name) VALUES( '{message.from_user.id}','{message.from_user.first_name}' )")

        db.commit()











#------------------------ Конец бота

def kb_main(message, text = "Сделайте Ваш выбор"):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Контакты")
    button2 = types.KeyboardButton("Режим работы")
    button3 = types.KeyboardButton("Локация")
    button4 = types.KeyboardButton("Заказать доставку")
    kb.add(button1,button2,button3, button4)
    bot.send_message(message.chat.id,text,reply_markup=kb)

def kb_main_1(message, text = "Сделайте Ваш выбор"):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Контакты")
    button2 = types.KeyboardButton("Режим работы")
    button3 = types.KeyboardButton("Локация")
    button4 = types.KeyboardButton("Начать сначала оформление доставки")
    kb.add(button1,button2,button3, button4)
    bot.send_message(message.chat.id,text,reply_markup=kb)
def kb_0(message, text = " Продолжайте работу "):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("  ")
    kb.add(button1)
    bot.send_message(message.chat.id,text,reply_markup=kb)



def kb_inline_1(message, text = "Выбираем машину"):
    kb = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Машина до 2т, до 12 м3", callback_data="1")
    button2 = types.InlineKeyboardButton("Манипулятор до 10т, 8 под", callback_data="2")
    #button2 = types.InlineKeyboardButton("Машина до 3.5т, до 18м3", callback_data="2")


    kb.add(button1,button2)
    bot.send_message(message.chat.id, text, reply_markup=kb)

def kb_inline_time(message, text = "Выберите время доставки"):
    kb = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("9.00-10.00", callback_data="9")
    button2 = types.InlineKeyboardButton("10.00-11.00", callback_data="10")
    button3 = types.InlineKeyboardButton("11.00-12.00", callback_data="11")
    button4 = types.InlineKeyboardButton("12.00-13.00", callback_data="12")
    button5 = types.InlineKeyboardButton("13.00-14.00", callback_data="13")
    button6 = types.InlineKeyboardButton("14.00-15.00", callback_data="14")
    button7 = types.InlineKeyboardButton("15.00-16.00", callback_data="15")
    button8 = types.InlineKeyboardButton("16.00-17.00", callback_data="16")
    button9 = types.InlineKeyboardButton("17.00-18.00", callback_data="17")
    button10 = types.InlineKeyboardButton("18.00-19.00", callback_data="18")
    button11 = types.InlineKeyboardButton("19.00-20.00", callback_data="19")

    kb.add(button1,button2,button3,button4,button5,button6,button7,button8,button9,button10,button11)
    bot.send_message(message.chat.id, text, reply_markup=kb)

def kb_inline_file(message, text = "Выберите вид заказа"):
    kb = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Загрузить фото заказа", callback_data="f")
    button2 = types.InlineKeyboardButton("Заказать звонок менеджера", callback_data="c")
    kb.add(button1,button2)
    bot.send_message(message.chat.id, text, reply_markup=kb)

def kb_inline_adres(message, text = "Проверка адреса"):
    kb = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Верно", callback_data="ok")
    button2 = types.InlineKeyboardButton("Ввести еще раз", callback_data="no_ok")
    kb.add(button1,button2)
    bot.send_message(message.chat.id, text, reply_markup=kb)

def kb_admin(message, text = "Сделайте Ваш выбор"):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Заказы по дате")
    button2 = types.KeyboardButton("Заказы по машинам")
    button3 = types.KeyboardButton("Справочник клиентов")
    kb.add(button1,button2,button3)
    bot.send_message(message.chat.id,text,reply_markup=kb)

def kb_admin_avto(message, text = "Сделайте Ваш выбор"):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Фиат")
    button2 = types.KeyboardButton("Скания")
    #button3 = types.KeyboardButton("Скания")
    kb.add(button1,button2)
    bot.send_message(message.chat.id,text,reply_markup=kb)

def server_1(text,call):
    db = sqlite3.connect("aleana_server.db")
    sql = db.cursor()
    sql.execute(f"UPDATE data SET time = '{text}' WHERE id_client = '{call.from_user.id}'")
    db.commit()

def server_2(text,message):
    db = sqlite3.connect("aleana_server.db")
    sql = db.cursor()
    for i in sql.execute(
            f"SELECT data.id_client, data.day, data.car, data.time, data.text, data.id_foto, dostavka.tel, dostavka.adress   "
            f"FROM dostavka INNER JOIN data ON dostavka.id_client = data.id_client WHERE car = '{text}'"):
        bot.send_message(message.chat.id, f"№ ID клиента - {i[0]},\nДата - {i[1]},\nМашина - {i[2]},\nВремя - {i[3]},"
                                          f"\nЗвонок  - {i[4]},\nТелефон - {i[6]},\nАдрес - {i[7]} ")
        if i[5]:
            bot.send_photo(message.chat.id, i[5])
        else:
            pass



@bot.message_handler(commands=['admin'])
def start_message(message):
    bot.send_message(message.chat.id, f"Добро день, {message.from_user.first_name}, Введите пароль")





@bot.message_handler(content_types=['text'])
def send_text(message):
    global wait_type
    text = message.text.lower()
    date_ok = "\d{1,2}.\d{1,2}.\d{4}"
    date_admin = "\d{1,2}-\d{1,2}-\d{4}"
    tel_ok = "^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"

    try:
        if text in ["привет", "добрый день", "здоров", "hello", "hi"]:
            bot.send_message(message.chat.id, f"Добрый день,{message.from_user.first_name}, рад Вас слышать")
        elif text == 'admin':
            bot.send_message(message.chat.id, f"Добрый день,{message.from_user.first_name}, Вы вошли, как администратор")
        elif text == "контакты":
            bot.send_message(message.chat.id, f"A1 - +375(44)760-88-90\nМТС - +375(33)380-88-90\nгород - 8(01716)9-05-05\nсайт - http://aleana.by/\ne-mail - weldbi@mail.ru")

        elif text == "режим работы":
            bot.send_message(message.chat.id, f"ПН-СБ - 8.00-20.00\nВС - 9.00-18.00\nБез обеда")



        elif text == "локация":
            bot.send_message(message.chat.id, f"г.Фаниполь, ул.Мира, 1А\nМагазин Алеана\nЛокация https://goo.gl/maps/FBhbzVAv6ZRpVxpb6")
        elif text == "6666":
            kb_admin(message)
        elif text == "заказы по дате":
            bot.send_message(message.chat.id, f"Введите  дату\nв формате ХХ-ХХ-ХХХХ,\nнапример 01-12-2023")



        elif text == "заказать доставку":
            #kb_inline_1(message)
           bot.send_message(message.chat.id, f"Введите желаемую дату\nв формате ХХ.ХХ.ХХХХ,\nнапример 01.12.2023")


        elif re.match(date_admin, text):
            bot.send_message(message.chat.id, "Печатаю заказы")
            b = text.replace('-', '.')

            db = sqlite3.connect("aleana_server.db")
            sql = db.cursor()

            for i in sql.execute(f"SELECT data.id_client, data.day, data.car, data.time, data.text, data.id_foto, dostavka.tel, dostavka.adress   "
                                 f"FROM dostavka INNER JOIN data ON dostavka.id_client = data.id_client WHERE day = '{b}'"):


                bot.send_message(message.chat.id,f"№ ID клиента - {i[0]},\nДата - {i[1]},\nМашина - {i[2]},\nВремя - {i[3]},"
                                                 f"\nЗвонок  - {i[4]},\nТелефон - {i[6]},\nАдрес - {i[7]} ")
                if i[5]:
                    bot.send_photo(message.chat.id, i[5] )
                else:
                    pass


        elif text == "заказы по машинам":
            kb_admin_avto(message)




        elif re.match(date_ok, text):
            kb_main_1(message)

            if datetime.datetime.strptime(text, "%d.%m.%Y") >=datetime.datetime.today():
                kb_inline_time(message)

                db = sqlite3.connect("aleana_server.db")
                sql = db.cursor()

                sql.execute(f"INSERT INTO data (id_client,day) VALUES( '{message.from_user.id}','{text}' )")

                db.commit()
            else:
                bot.send_message(message.chat.id, "Не верный ввод даты")




        elif re.match(tel_ok, text):
            db = sqlite3.connect("aleana_server.db")
            sql = db.cursor()
            sql.execute(f"UPDATE client SET tel = '{text}' WHERE id = '{message.from_user.id}'")
            sql.execute(f"UPDATE dostavka SET tel = '{text}' WHERE id_client = '{message.from_user.id}'")


            db.commit()
            bot.send_message(message.chat.id, "Телефон для связи принят")

            bot.send_message(message.chat.id, "Введите ваш адрес")
            wait_type = 1 # ждем ввода адреса


        elif text == "начать сначала оформление доставки":
            kb_main(message)


        elif text == "фиат":
            server_2(text, message)
        #elif text == "мерседес":
            #server_2(text,message)

        elif text == "скания":
            server_2(text,message)


        elif text == "справочник клиентов":

            db = sqlite3.connect("aleana_server.db")
            sql = db.cursor()
            for i in sql.execute(f"SELECT * FROM client "):

                bot.send_message(message.chat.id,f"Id клиента - {i[0]},\nИмя клиента - {i[1]},\nТелефон - {i[2]}")
            kb_admin(message)

        elif wait_type == 1:
            b= text
            bot.send_message(message.chat.id, f"Проверьте ваш адрес:\n{text}")
            db = sqlite3.connect("aleana_server.db")
            sql = db.cursor()
            sql.execute(f"UPDATE dostavka SET adress = '{b}' WHERE id_client = '{message.from_user.id}'")
            db.commit()
            kb_inline_adres(message)
            wait_type = 0  # обнуляем ожидание







        else:
            bot.send_message(message.chat.id, f"{message.from_user.first_name}, введены не верные данные, сделайте свой выбор")

    except Exception:
        bot.send_message(message.chat.id, "Вы ввели некорректные данные")


@bot.message_handler(content_types=['sticker'])
def get_stiker(message):
    bot.send_message(message.chat.id, "Классный стикер! ")

@bot.callback_query_handler(func = lambda call: True)
def callback_InLine(call):
    global wait_type
    if call.message:
        text = call.data
        if text == "1":
            bot.send_message(call.message.chat.id, "Фиат Дукато АХ4299-5 приедет к Вам")
            bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
            kb_inline_file(call.message)

            db = sqlite3.connect("aleana_server.db")
            sql = db.cursor()
            sql.execute(f"UPDATE data SET car = 'фиат' WHERE id_client = '{call.from_user.id}'")
            db.commit()



        elif text == "2":
            bot.send_message(call.message.chat.id, "Манипулятор Скания АТ2657-5 приедет к Вам")
            bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
            kb_inline_file(call.message)

            db = sqlite3.connect("aleana_server.db")
            sql = db.cursor()
            sql.execute(f"UPDATE data SET car = 'скания' WHERE id_client = '{call.from_user.id}'")
            db.commit()

        #elif text == "3":
            #bot.send_message(call.message.chat.id, "Манипулятор Скания АТ2657-5 приедет к Вам")
            #bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
            #kb_inline_file(call.message)

            #db = sqlite3.connect("aleana_server.db")
            #sql = db.cursor()
            #sql.execute(f"UPDATE data SET car = 'скания' WHERE id_client = '{call.from_user.id}'")
            #db.commit()

        elif text == "9":
            bot.send_message(call.message.chat.id, "9 - 10")
            bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
            kb_inline_1(call.message)
            server_1(text,call)



        elif text == "10":
                bot.send_message(call.message.chat.id, "10 - 11")
                bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
                kb_inline_1(call.message)
                server_1(text, call)
        elif text == "11":
                bot.send_message(call.message.chat.id, "11 - 12")
                bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
                kb_inline_1(call.message)
                server_1(text,call)
        elif text == "12":
                bot.send_message(call.message.chat.id, "12 - 13")
                bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
                kb_inline_1(call.message)
                server_1(text,call)
        elif text == "13":
                bot.send_message(call.message.chat.id, "13 - 14")
                bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
                kb_inline_1(call.message)
                server_1(text,call)
        elif text == "14":
                bot.send_message(call.message.chat.id, "14 - 15")
                bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
                kb_inline_1(call.message)
                server_1(text,call)
        elif text == "15":
                bot.send_message(call.message.chat.id, "15 - 16")
                bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
                kb_inline_1(call.message)
                server_1(text,call)
        elif text == "16":
                bot.send_message(call.message.chat.id, "16 - 17")
                bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
                kb_inline_1(call.message)
                server_1(text,call)
        elif text == "17":
                bot.send_message(call.message.chat.id, "17 - 18")
                bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
                kb_inline_1(call.message)
                server_1(text,call)
        elif text == "18":
                bot.send_message(call.message.chat.id, "18 - 19")
                bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
                kb_inline_1(call.message)
                server_1(text,call)
        elif text == "19":
                bot.send_message(call.message.chat.id, "19 - 20")
                bot.edit_message_text("Продолжаем", call.message.chat.id, call.message.message_id, reply_markup=None)
                kb_inline_1(call.message)
                server_1(text, call)
        elif text == "f":
            bot.edit_message_text("Загрузите фото заказа", call.message.chat.id, call.message.message_id, reply_markup=None)
        elif text == "c":
            bot.edit_message_text("Звонок менеджера", call.message.chat.id, call.message.message_id, reply_markup=None)
            db = sqlite3.connect("aleana_server.db")
            sql = db.cursor()
            sql.execute(f"UPDATE data SET text = 'Перезвонить' WHERE id_client = '{call.from_user.id}'")
            sql.execute(f"UPDATE data SET id_foto = '' WHERE id_client = '{call.from_user.id}'")

            db.commit()

            bot.send_message(call.message.chat.id, f"Введите номер телефона\nВ формате 8(xxx)xxx-xx-xx\nбез пробелов")

        elif text == "ok":
            bot.edit_message_text("Спасибо за Ваш заказ, мы обязательно свяжемся с Вами.", call.message.chat.id, call.message.message_id, reply_markup=None)
            bot.send_message(477068883, f"Есть заказ")
            db = sqlite3.connect("aleana_server.db")
            sql = db.cursor()
            a = call.message.chat.id


            for i in sql.execute(
                    f"SELECT data.id_client, data.day, data.car, data.time, data.text, data.id_foto, dostavka.tel, dostavka.adress   "
                    f"FROM dostavka INNER JOIN data ON dostavka.id_client = data.id_client WHERE data.id_client = '{a}'"):

                bot.send_message(477068883,
                                 f"№ ID клиента - {i[0]},\nДата - {i[1]},\nМашина - {i[2]},\nВремя - {i[3]},"
                                 f"\nЗвонок  - {i[4]},\nТелефон - {i[6]},\nАдрес - {i[7]} ")
                if i[5]:
                    bot.send_photo(477068883, i[5])
                else:
                    pass




        elif text == "no_ok":
            bot.send_message(call.message.chat.id, f"Введите еще раз Ваш адрес")
            wait_type = 1




        else:
            bot.send_message(call.message.chat.id,"Опа что-то пошло не так....")

@bot.message_handler(content_types=["photo"])
def photo(message):



    idphoto = message.photo[0].file_id
    db = sqlite3.connect("aleana_server.db")
    sql = db.cursor()

    sql.execute(f"UPDATE data SET id_foto = '{idphoto}' WHERE id_client = '{message.from_user.id}'")
    sql.execute(f"UPDATE data SET text = 'Есть фото' WHERE id_client = '{message.from_user.id}'")
    db.commit()
    bot.send_message(message.chat.id, f"Введите номер телефона\nВ формате 8(xxx)xxx-xx-xx\nбез пробелов")



bot.polling(none_stop=True)



