import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start'.
@bot.message_handler(commands=['start'])
def comand_start(message: telebot.types.Message):
    bot.reply_to(message, f'Приветствую, {message.chat.username}!\n Я Бот-Конвертер, который конвертирует валюту и я могу выполнять следующие команды:\n - Посмотреть, что я могу через команду /help \n - Показать список доступных валют через команду /values \
    \n- Конвертировать валюту через команду <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n')

# Обрабатываются все сообщения, содержащие команды '/help'.
@bot.message_handler(commands=['help'])
def comand_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в формате: <имя валюты> \ \
    <в какую валюту перевести> \ <количество переводимой валюты>  \
     Пример: рубль евро 2\n Доступные валюты можно посмотреть по команде: /values'
    bot.reply_to(message, text)


# Обрабатываются все сообщения, содержащие команды '/values'.
@bot.message_handler(commands=['values'])
def comand_value(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys:
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


# Обрабатываются запросы конвертирования.
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise APIException('Необходимо ввести 3 параметра.\nПример: рубль евро 1')

        quote, base, amount = value
        total_base = CryptoConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка на стороне пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)