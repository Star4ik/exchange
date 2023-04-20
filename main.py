import os
import telebot
from dotenv import load_dotenv
from extensions import APIException, Converter
from config import exchanges
import traceback


load_dotenv(".env")

_token = os.getenv("TOKEN")

converter_bot = telebot.TeleBot(_token)


@converter_bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Приветствие!"
    converter_bot.send_message(message.chat.id, text)


@converter_bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    converter_bot.reply_to(message, text)


@converter_bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        quote, base, amount = values
        answer = Converter.get_price(*values)
    except APIException as e:
        converter_bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        converter_bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        converter_bot.reply_to(message, answer)


converter_bot.polling()