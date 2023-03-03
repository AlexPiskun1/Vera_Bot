# vera_piskun_bot  Бот отвечает на часто задаваемые вопросы
import telebot
from telebot import types

import sqlite3
import re

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

@bot.message_handler(content_types=['sticker'])
def get_stiker(message):
    bot.send_message(message.chat.id, "Классный стикер! ")

@bot.message_handler(commands=['admin'])
def start_message(message):
    bot.send_message(message.chat.id, f"Добро день, {message.from_user.first_name}, Введите пароль")

def kb_main(message, text = "Сделайте Ваш выбор"):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Обо мне")
    button2 = types.KeyboardButton("Мои работы")
    button3 = types.KeyboardButton("Цены")
    button4 = types.KeyboardButton("Отзывы")
    button5 = types.KeyboardButton("Instagram")
    button6 = types.KeyboardButton("Контакты")
    button7 = types.KeyboardButton("Запись")
    kb.add(button1,button2,button3, button4,button5,button6,button7)
    bot.send_message(message.chat.id,text,reply_markup=kb)




def kb_admin(message, text = "Сделайте Ваш выбор"):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Справочник клиентов")
    button2 = types.KeyboardButton("Вернуться в главное меню")
    kb.add(button1,button2)
    bot.send_message(message.chat.id,text,reply_markup=kb)

def kb_text(message, text = "Все верно введено? "):
    kb = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Да", callback_data="да")
    button2 = types.InlineKeyboardButton("Написать еще раз", callback_data="нет")
    kb.add(button1,button2)
    bot.send_message(message.chat.id, text, reply_markup=kb)

def kb_text_phone(message, text = "Верный номер? "):
    kb = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Да", callback_data="да1")
    button2 = types.InlineKeyboardButton("Написать еще раз", callback_data="нет1")
    kb.add(button1,button2)
    bot.send_message(message.chat.id, text, reply_markup=kb)


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
        elif text == "обо мне":
            bot.send_message(message.chat.id, f"http://verapiskun.visual.tilda.ws/page28492284.html?fbclid=PAAabbRm1NSuds1JGtavg_mcMMu03wOXAsH8V3tFReh1MnHvENaNBiM8_Ov-0#about")
        elif text == "мои работы":
            bot.send_message(message.chat.id, f"http://verapiskun.visual.tilda.ws/page28492284.html?fbclid=PAAabbRm1NSuds1JGtavg_mcMMu03wOXAsH8V3tFReh1MnHvENaNBiM8_Ov-0#rec462471181")
        elif text == "цены":
            bot.send_message(message.chat.id, f"http://verapiskun.visual.tilda.ws/page28492284.html?fbclid=PAAabbRm1NSuds1JGtavg_mcMMu03wOXAsH8V3tFReh1MnHvENaNBiM8_Ov-0#rec460415457")
        elif text == "отзывы":
            bot.send_message(message.chat.id, f"http://verapiskun.visual.tilda.ws/page28492284.html?fbclid=PAAabbRm1NSuds1JGtavg_mcMMu03wOXAsH8V3tFReh1MnHvENaNBiM8_Ov-0#rec462477331")
        elif text == "instagram":
            bot.send_message(message.chat.id, f"https://instagram.com/verapiskun.ph?igshid=YmMyMTA2M2Y=")
        elif text == "контакты":
            bot.send_message(message.chat.id, f"Телефон: +48 451 604 992 \ne-mail: v_piskun@internet.ru \nViber +375 558 27 78 \nTelegram +375 558 27 78")
        elif text == "запись":
            bot.send_message(message.chat.id,f"Введите желаемую дату и формат съемки. В ближайшее время я свяжусь с вами и мы все обсудим.")
            wait_type = 1  # ждем ввода текста


        elif text == "6666":
            kb_admin(message)
        elif text == "справочник клиентов":

            db = sqlite3.connect("vera_piskun_server.db")
            sql = db.cursor()
            for i in sql.execute(f"SELECT * FROM client "):

                bot.send_message(message.chat.id,f"Id клиента - {i[0]},\nИмя клиента - {i[1]},\nТелефон - {i[2]},\nТекст - {i[3]}")
            kb_admin(message)

        elif text == "вернуться в главное меню":
            kb_main(message)


        elif wait_type == 1:
            b= text
            bot.send_message(message.chat.id, f"Проверьте ваш запрос:\n{b}")
            db = sqlite3.connect("vera_piskun_server.db")
            sql = db.cursor()
            sql.execute(f"UPDATE client SET text = '{b}' WHERE id = '{message.from_user.id}'")
            db.commit()
            kb_text(message)
            wait_type = 0  # обнуляем ожидание
        elif wait_type == 2:
            b= text
            bot.send_message(message.chat.id, f"Проверьте ваш запрос:\n{b}")
            db = sqlite3.connect("vera_piskun_server.db")
            sql = db.cursor()
            sql.execute(f"UPDATE client SET tel = '{b}' WHERE id = '{message.from_user.id}'")
            db.commit()
            kb_text_phone(message)
            wait_type = 0  # обнуляем ожидание























        else:
            bot.send_message(message.chat.id, f"{message.from_user.first_name}, введены не верные данные, сделайте свой выбор")

    except Exception:
        bot.send_message(message.chat.id, "Вы ввели некорректные данные")

@bot.callback_query_handler(func = lambda call: True)
def callback_InLine(call):
    global wait_type
    if call.message:
        text = call.data

        if text == "да":
            bot.send_message(call.message.chat.id, f"Введите номер телефона")
            wait_type = 2

        elif text == "нет":
            bot.send_message(call.message.chat.id, f"Введите еще раз")
            wait_type = 1
        if text == "да1":
            bot.send_message(call.message.chat.id, f"Я скоро свяжусь в Вами")
            bot.send_message(785844839, f"Есть сообщение от Бота")
            db = sqlite3.connect("vera_piskun_server.db")
            sql = db.cursor()
            a = call.message.chat.id

            for i in sql.execute(f"SELECT * FROM client WHERE id = {a} "):

                bot.send_message(785844839,f"Id клиента - {i[0]},\nИмя клиента - {i[1]},\nТелефон - {i[2]},\nТекст - {i[3]}")


            wait_type = 0



        elif text == "нет1":
            bot.send_message(call.message.chat.id, f"Введите еще раз")
            wait_type = 2


bot.polling(none_stop=True)



