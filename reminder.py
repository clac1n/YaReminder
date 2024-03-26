import telebot
from telebot import types
import datetime
import pytz
import logging

# Set up logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = '*'
bot = telebot.TeleBot(TOKEN)

reminder_sent = False

def send_reminder(chat_id):
    global reminder_sent
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton('Понял')
    markup.add(button)

    bot.send_message(chat_id, 'Котлету в размере 175 рублей на базу(Сбер) Сашке пжпжпжппж!', reply_markup=markup)
    logging.info(f"Reminder sent to chat ID: {chat_id}")

    while not reminder_sent:
        time.sleep(60)
        bot.send_message(chat_id, 'Хеллоу. Я чучело, которое было создано для того, чтобы напоминать тебе о том что Сашке надо на Сбер скинуть 175 рублей 14-го числа каждого месяца до конца жизни.\n\n14-го числа с 12:00 бот будет отправлять тебе напоминание каждый час, пока не нажмешь кнопку "Понял". На самом деле код было бы писать легче без этой, но Леха даже бота может заигнорить. Надеюсь хотя бы это поможет.\n\nСоветую нажимать кнопку "Понял", когда уже переведёте бабосики. И НЕ ВЫКЛЮЧАТЬ УВЕДОМЛЕНИЯ, А ЕСЛИ ВЫКЛЮЧЕНЫ ТО ВКЛЮЧИТЬ\n\nP.S. После того как нажмёте кнопку "Понял" бот отправит ещё 1 напоминание и после перестанет. Мне слишком впадлу фиксить это.', reply_markup=markup)
        logging.info(f"Reminder resent to chat ID: {chat_id}")

def check_time():
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tz)
    target_time = now.replace(hour=12, minute=1, second=0, microsecond=0)
    return now.day == 14 and now >= target_time

@bot.message_handler(commands=['start'])
def start_message(message):
    global reminder_sent
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton('Начать')
    markup.add(button)

    bot.send_message(message.chat.id, 'Привет! Я бот-напоминалка, созданный, чтобы ты не забывал скидывать 175 рублей Сашке на Сбер 14-го числа каждого месяца.', reply_markup=markup)
    logging.info(f"Start message sent to chat ID: {message.chat.id}")

    while True:
        if check_time() and not reminder_sent:
            send_reminder(message.chat.id)
        time.sleep(60)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global reminder_sent
    if message.text == 'Начать':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEJp3tkrG3TFEY22VyHu-VniBtBSq37gQACUiIAAiepcErGXOlKPwIibi8E')
        bot.send_message(message.chat.id, 'Ждем-с', reply_markup=types.ReplyKeyboardRemove())
        logging.info(f"User started reminder in chat ID: {message.chat.id}")

        if check_time() and not reminder_sent:
            send_reminder(message.chat.id)

        while True:
            if not check_time():
                break
            if not reminder_sent:
                send_reminder(message.chat.id)
            time.sleep(60)
    elif message.text == 'Понял':
        bot.send_message(message.chat.id, 'Услышал. Увидимся через месяц. Помни, что я тупой и отправлю еще одно напоминание, но потом перестану', reply_markup=types.ReplyKeyboardRemove())
        reminder_sent = True
        logging.info(f"User acknowledged reminder in chat ID: {message.chat.id}")
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю.')
        logging.info(f"Unrecognized message from chat ID: {message.chat.id}")

while True:
    try:
        bot.polling()
    except Exception as e:
        logging.error(f"An error occurred: {e}. Reconnecting...")
