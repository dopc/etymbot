import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import InlineQueryHandler
import time
from bs4 import BeautifulSoup
import requests
import logging


bot = telegram.Bot(token= <my lovely token>)
updater = Updater(token= <my lovely token>)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

SEARCH_URL = 'https://www.etymonline.com/search?q='

from telegram import InlineQueryResultArticle, InputTextMessageContent
def inline_etym(bot,update):
    query = update.inline_query.query
    result = []
    text = first_result_return(query)
    result.append(InlineQueryResultArticle(
        id=query,
        title=query,
        input_message_content=InputTextMessageContent(query + ': \n' + text)))

    bot.answer_inline_query(update.inline_query.id, result)

inline_etym_handler = InlineQueryHandler(inline_etym)
dispatcher.add_handler(inline_etym_handler)
updater.start_polling()


'''
functions from https://github.com/tetrismegistus/etym
''' 
def soup_search(search_term):
    # post request to search URL, return beautiful soup parsed object
    url = SEARCH_URL + search_term
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def first_result_return(word):
    #print("{}\n".format(search_page.find("div", class_="searchList__pageCount--2jQdB").get_text()))
    search_page = soup_search(word)
    return search_page.find("section", class_="word__defination--2q7ZH undefined").get_text()
