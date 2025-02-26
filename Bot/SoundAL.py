import telebot
from openai import OpenAI
from gtts import gTTS
import os
import uuid

client = OpenAI(
    api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I",
    base_url="https://api.proxyapi.ru/openai/v1",
)

bot_token = '7295302512:AAHQyKsMXXOe3J-7BUXjXNrBf5HdZiACwlQ'  # Замените на токен вашего бота
bot = telebot.TeleBot(bot_token)

user_chats = {}


def chat_with_ai(user_id, initial_message):
    messages = user_chats.get(user_id, [])
    messages.append({"role": "user", "content": initial_message})

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    response_message = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response_message})
    user_chats[user_id] = messages

    return response_message


def text_to_speech(text):
    # Создание временного файла с аудио
    temp_filename = f'temp_{uuid.uuid4()}.mp3'
    tts = gTTS(text=text, lang='ru')  # Убедитесь, что установлен нужный язык
    tts.save(temp_filename)
    return temp_filename


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = message.from_user.id
    response = chat_with_ai(user_id, message.text)

    # Преобразуем текст в речь
    audio_file = text_to_speech(response)

    # Отправляем голосовое сообщение пользователю
    with open(audio_file, 'rb') as voice:
        bot.send_voice(user_id, voice)

    # Удаляем временный файл
    os.remove(audio_file)


if __name__ == "__main__":
    bot.polling(none_stop=True)