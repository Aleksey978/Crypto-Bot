import telebot
from config import TOKEN, keys
from extensions import CryptoConverter, ConvertionException




bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id,
                     f"Здравствуйте {message.chat.username} добро пожаловать в чат Бот где вы сможете узнать курс по обмену популярной крипловалюты \n "
                     f"Правила пользования чатом: \n Введите \n <имя валюты, цену которой он хочет узнать>\n <имя валюты, в которой надо узнать цену первой валюты> \n<количество первой валюты>.")


@bot.message_handler(commands=['value'])
def value(message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException("Неверные параметры")
        quote, base, amount = values
        quote, base = quote.lower(), base.lower()
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя \n {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n")
    else:
        text = f'Цена за {amount} {keys[quote]} равна {total_base} {keys[base]}'
        bot.reply_to(message, text)



bot.polling(none_stop=True)
