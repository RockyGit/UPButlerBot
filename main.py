import telebot
# import PgSQL
import re
import config

bot = telebot.TeleBot(config.token)

# post = PgSQL.PostgreSQL()

@bot.message_handler(commands=['start', 'help'])
def start(message):
	bot.send_message(message.chat.id,'Вас приветствует пикабот. Возможные команды: \r\n 1. ')

# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def find(message):
#     st = message.text.split(' ')
#     rows_fiz = post.select_like_fiz(st)
#     rows_ur = post.select_like_ur(st)


if __name__ == '__main__':
	bot.polling(none_stop=True)