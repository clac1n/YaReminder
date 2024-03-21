import telebot
from telebot import types
import datetime
import pytz
import time

TOKEN = ' *****************TOKEN************* '
bot = telebot.TeleBot(TOKEN)

reminder_sent = False

def send_reminder(chat_id):
    global reminder_sent
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton('Понял')
    markup.add(button)
    bot.send_message(chat_id, 'Котлету в размере 175 рублей на базу(Сбер) Сашке пжпжпжппж!', reply_markup=markup)
    while not reminder_sent:
        time.sleep(60)
        bot.send_message(chat_id, 'Котлету в размере 175 рублей на базу(Сбер) Сашке пжпжпжппж!', reply_markup=markup)

def reset_reminder():
    global reminder_sent
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tz)
    if now.day == 1:
        reminder_sent = False

def check_time():
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tz)
    target_time = now.replace(hour=12, minute=1, second=0, microsecond=0)
    if now.day == 14 and now >= target_time:
        return True
    return False

@bot.message_handler(commands=['start'])
def start_message(message):
    global reminder_sent
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton('Начать')
    markup.add(button)
    bot.send_message(message.chat.id, 'Хеллоу. Я чучело, которое было создано для того, чтобы напоминать тебе о том что Сашке надо на Сбер скинуть 175 рублей 14-го числа каждого месяца до конца жизни.\n\n14-го числа с 12:00 бот будет отправлять тебе напоминание каждый час, пока не нажмешь кнопку "Понял". На самом деле код было бы писать легче без этой хуйни, но Леха даже бота может заигнорить. Надеюсь хотя бы это поможет.\n\nСоветую нажимать кнопку "Понял", когда уже переведёте бабосики. И НЕ ВЫКЛЮЧАТЬ УВЕДОМЛЕНИЯ, А ЕСЛИ ВЫКЛЮЧЕНЫ ТО ВКЛЮЧИТЬ НАХУЙ\n\nP.S. После того как нажмёте кнопку "Понял" бот отправит ещё 1 напоминание и после перестанет. Мне слишком впадлу фиксить эту хуйню.', reply_markup=markup)
    while True:
        reset_reminder()
        if check_time() and not reminder_sent:
            send_reminder(message.chat.id)
        time.sleep(60)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global reminder_sent
    if message.text == 'Начать':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEJp3tkrG3TFEY22VyHu-VniBtBSq37gQACUiIAAiepcErGXOlKPwIibi8E')
        bot.send_message(message.chat.id, 'Ждём-с', reply_markup=types.ReplyKeyboardRemove())
        if check_time() and not reminder_sent:
            send_reminder(message.chat.id)
        while True:
            reset_reminder()
            time.sleep(60)
            if not check_time():
                break
            if not reminder_sent:
                send_reminder(message.chat.id)
    elif message.text == 'Понял':
        bot.send_message(message.chat.id, 'Услышал. Увидимся через месяц. Помни, что я тупой и отправлю еще одно напоминание, но потом перестану.', reply_markup=types.ReplyKeyboardRemove())
        reminder_sent = True
    else:
        bot.send_message(message.chat.id, 'Услышал. Увидимся через месяц. Помни, что я тупой и отправлю еще одно напоминание, но потом перестану.')

bot.polling()
