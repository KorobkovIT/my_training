import telebot

# Замените 'YOUR_API_TOKEN' на ваш токен от BotFather
API_TOKEN = '7295302512:AAHQyKsMXXOe3J-7BUXjXNrBf5HdZiACwlQ'
bot = telebot.TeleBot(API_TOKEN)


# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Добро пожаловать! Я ваш помощник-бот. Используйте команду /help для получения справочной информации.")


# Обработка команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Доступные команды:\n"
        "/start - Запустить бота\n"
        "/help - Получить справочную информацию\n"
        "/perevorot <ваш текст> - Перевернуть текст\n"
        "/caps <ваш текст> - Преобразовать текст в заглавные буквы\n"
        "/cut <ваш текст> - Удалить все гласные буквы из текста\n"
        "/safe < логин > < пароль > - принимает логин и пароль, разделенные пробелом, и сохраняет их в хранилище\n"
        "/getpass < логин > - позволяет получить соответствующий пароль по логину"

    )
    bot.reply_to(message, help_text)


# Обработка команды /perevorot
@bot.message_handler(commands=['perevorot'])
def reverse_text(message):
    # Получаем текст после команды /perevorot
    text_to_reverse = message.text[len('/perevorot '):].strip()

    if text_to_reverse:
        reversed_text = text_to_reverse[::-1]  # Переворачиваем текст
        bot.reply_to(message, reversed_text)
    else:
        bot.reply_to(message, "Пожалуйста, введите текст для переворота после команды /perevorot.")


# Обработка команды /caps
@bot.message_handler(commands=['caps'])
def caps_text(message):
    # Получаем текст после команды /caps
    text_to_caps = message.text[len('/caps '):].strip()

    if text_to_caps:
        caps_text = text_to_caps.upper()  # Преобразуем текст в заглавные буквы
        bot.reply_to(message, caps_text)
    else:
        bot.reply_to(message, "Пожалуйста, введите текст для преобразования в заглавные буквы после команды /caps.")


# Обработка команды /cut
@bot.message_handler(commands=['cut'])
def cut_vowels(message):
    # Получаем текст после команды /cut
    text_to_cut = message.text[len('/cut '):].strip()

    if text_to_cut:
        vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯaeiouAEIOU"
        cut_text = ''.join([char for char in text_to_cut if char not in vowels])

# Удаляем гласные
        bot.reply_to(message, cut_text)
    else:
        bot.reply_to(message, "Пожалуйста, введите текст для удаления гласных после команды /cut.")

# Хранилище для логинов и паролей
user_credentials = {}

# Обработка команды /safe
@bot.message_handler(commands=['safe'])
def save_credentials(message):
    try:
        # Получаем аргументы команды
        _, username, password = message.text.split()
        user_credentials[username] = password
        bot.reply_to(message, f"Логин и пароль для '{username}' успешно сохранены.")
    except ValueError:
        bot.reply_to(message, "Ошибка: Пожалуйста, используйте формат: /safe <логин> <пароль>")

# Обработка команды /getpass
@bot.message_handler(commands=['getpass'])
def get_password(message):
    try:
        # Получаем аргументы команды
        _, username = message.text.split()
        if username in user_credentials:
            password = user_credentials[username]
            bot.reply_to(message, f"Пароль для '{username}': {password}")
        else:
            bot.reply_to(message, f"Нет сохраненного пароля для логина '{username}'.")
    except ValueError:
        bot.reply_to(message, "Ошибка: Пожалуйста, используйте формат: /getpass <логин>")

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)