from telegram.ext import Updater
from telegram.ext import InlineQueryHandler
from bs4 import BeautifulSoup
import requests
import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent

updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

SEARCH_URL = 'https://www.etymonline.com/search?q='


def inline_etym(update, context):
    query = update.inline_query.query
    results = list()
    text = first_result_return(query)
    results.append(InlineQueryResultArticle(
        id=query,
        title=query,
        input_message_content=InputTextMessageContent(query + ': \n' + text)))

    context.bot.answer_inline_query(update.inline_query.id, results)


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
    search_page = soup_search(word)
    return search_page.find("section", class_="word__defination--2q7ZH undefined").get_text()
