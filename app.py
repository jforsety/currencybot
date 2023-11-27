import telebot
from config import keys, TOKEN
from extensions import ConvertionException, Converter

bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start'
@bot.message_handler(commands=['start', ])
def start(message: telebot.types.Message):
    text = """Данный бот позволяет конвертировать значения из денежных единиц одной страны, в единицы другой.\n
Увидеть примеры выполнения запроса можно командой: /help\n
Увидеть список всех доступных валют: /values\n
Узнать о создателе бота можно командой: /about
"""
    bot.reply_to(message, text)


# Обрабатываются все сообщения, содержащие команды '/help'
@bot.message_handler(commands=['help', ])
def help(message: telebot.types.Message):
    text = """Чтобы начать работу введите команду бота в следующем формате:\n
    <имя валюты><в какую валюту перевести> 
    <количество переводимой валюты>\nУвидеть список всех доступных валют: /values"""
    bot.reply_to(message, text)


# Обрабатывается команда /values. Вывод доступных валют.
@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)


# Обрабатывается команда /about. О нас.
@bot.message_handler(commands=['about', ])
def about(message: telebot.types.Message):
    text = """Классно что ты сюда зашел))\n
Пользуйся ботом, он будет развиваться и расти)"""
    text1 = """Дублирую команды, не потеряй: /start , /help, /values, /about"""
    bot.reply_to(message, text)
    with open("img/stiker.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo)
    bot.reply_to(message, text1)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise ConvertionException("Слишком много параметров")
        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
