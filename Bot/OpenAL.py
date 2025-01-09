import telebot
from openai import OpenAI

# Инициализация клиента API
client = OpenAI(
    api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I",
    base_url="https://api.proxyapi.ru/openai/v1",
)

# Инициализация бота
bot_token = '7295302512:AAHQyKsMXXOe3J-7BUXjXNrBf5HdZiACwlQ'  # Замените на токен вашего бота
bot = telebot.TeleBot(bot_token)

# Словарь для хранения сообщений по чатам
user_chats = {}


def chat_with_ai(user_id, initial_message):
    messages = user_chats.get(user_id, [])
    messages.append({"role": "user", "content": initial_message})

    # Отправка запроса к нейросети
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # Получение ответа нейросети
    response_message = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response_message})
    user_chats[user_id] = messages

    return response_message


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = message.from_user.id
    response = chat_with_ai(user_id, message.text)
    bot.reply_to(message, response)


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)