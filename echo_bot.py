#!/usr/bin/env python3
import json
import logging
import os
import types

import telebot
from telebot import types

from config import API_TOKEN
# from config_template import API_TOKEN


bot = telebot.TeleBot(API_TOKEN)

name = ''
surname = ''
age = 0

log = logging.getLogger('bot')


def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('log/echo_bot.log')
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)


@bot.message_handler(content_types=['text'])
def start(message):
    log.debug(f'{message}')
    if message.text == "/reg":
        bot.send_message(message.from_user.id, 'Как тебя зовут?')
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Введите команду /reg')


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Как у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:
        try:
            age = int(message.text)
        except Exception as exc:
            bot.send_message(message.from_user.id, 'Цифрам, пожалуйста')
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        if call.data == "yes":
            bot.send_message(call.message.chat.id, 'Запомню : )')
        elif call.data == "no":
            start(call.message)
    except Exception as exc:
        log.exception(f'нажатие на NO выдало {exc}')


if __name__ == '__main__':
    configure_logging()
    bot.polling(none_stop=True, interval=0)
