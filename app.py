import telebot
import os
from flask import Flask
import threading

TOKEN = os.environ.get(8320084044:AAGBwRFEs9TAiVsAqikJ9kn_vj7aeQdfsOg)
ADMIN_ID = os.environ.get(1873610199)

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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Здравствуйте! Я бот-помощник.\n/help - команды\n/order - оставить заявку")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "📋 Команды:\n/start - начать\n/help - справка\n/order - заявка")

@bot.message_handler(commands=['order'])
def ask_order(message):
    msg = bot.reply_to(message, "📝 Напишите ваше имя и телефон:")
    bot.register_next_step_handler(msg, process_order)

def process_order(message):
    if ADMIN_ID:
        bot.send_message(ADMIN_ID, f"📬 НОВАЯ ЗАЯВКА!\n\nОт: @{message.from_user.username}\nДанные: {message.text}")
    bot.reply_to(message, "✅ Спасибо! Мы свяжемся с вами.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "❌ Напишите /order, чтобы оставить заявку")

def run_bot():
    print("🤖 Бот запущен и работает!")
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
