import telebot
import os
from flask import Flask
import threading
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не задан")

if ADMIN_ID:
    ADMIN_ID = int(ADMIN_ID)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Бот работает"

@app.route('/health')
def health():
    return "ОК", 200

def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("📝 Оставить заявку"))
    keyboard.add(KeyboardButton("💰 Узнать цену"))
    keyboard.add(KeyboardButton("📍 Наш адрес"))
    keyboard.add(KeyboardButton("🕐 Время работы"))
    keyboard.add(KeyboardButton("❓ Помощь"))
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Здравствуйте! Я бот-помощник.\n\nНажмите на кнопку ниже, чтобы оставить заявку.", reply_markup=main_keyboard())

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "📋 Нажмите кнопку 'Оставить заявку' или выберите нужный пункт меню", reply_markup=main_keyboard())

@bot.message_handler(commands=['order'])
def ask_order(message):
    msg = bot.reply_to(message, "📝 Напишите ваше имя и телефон:")
    bot.register_next_step_handler(msg, process_order)

@bot.message_handler(commands=['price'])
def send_price(message):
    bot.reply_to(message, "💰 Стоимость услуг: от 1000 до 5000 рублей.\nТочную цену уточняйте по заявке.", reply_markup=main_keyboard())

@bot.message_handler(commands=['address'])
def send_address(message):
    bot.reply_to(message, "📍 Наш адрес: г. Москва, ул. Примерная, д. 10", reply_markup=main_keyboard())

@bot.message_handler(commands=['worktime'])
def send_worktime(message):
    bot.reply_to(message, "🕐 Мы работаем: Пн-Пт с 9:00 до 21:00, Сб-Вс с 10:00 до 18:00", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == "📝 Оставить заявку")
def button_order(message):
    ask_order(message)

@bot.message_handler(func=lambda message: message.text == "💰 Узнать цену")
def button_price(message):
    send_price(message)

@bot.message_handler(func=lambda message: message.text == "📍 Наш адрес")
def button_address(message):
    send_address(message)

@bot.message_handler(func=lambda message: message.text == "🕐 Время работы")
def button_worktime(message):
    send_worktime(message)

@bot.message_handler(func=lambda message: message.text == "❓ Помощь")
def button_help(message):
    send_help(message)

def process_order(message):
    if ADMIN_ID:
        bot.send_message(ADMIN_ID, f"📬 НОВАЯ ЗАЯВКА!\n\nОт: @{message.from_user.username}\nДанные: {message.text}")
    bot.reply_to(message, "✅ Спасибо! Мы свяжемся с вами.", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "❌ Нажмите на кнопку ниже", reply_markup=main_keyboard())

def run_bot():
    print("🤖 Бот запущен и работает!")
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
