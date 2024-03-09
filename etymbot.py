from telegram.ext import Updater
from telegram.ext import InlineQueryHandler
from bs4 import BeautifulSoup
import requests
import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent
import os

logger = logging.getLogger(__name__)

updater = Updater(token=os.getenv("BOT_TOKEN"))
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
SEARCH_URL = 'https://www.etymonline.com/search?q='


def inline_etym(update, context):
    query = update.inline_query.query
    try:
        logger.info(f"Query: {query}")
        results = list()
        text = first_result_return(query)
        content = f"{query}:\n{text}"
        results.append(InlineQueryResultArticle(
            id=query,
            title=query,
            input_message_content=InputTextMessageContent(content))
        )
        context.bot.answer_inline_query(update.inline_query.id, results)
    except AttributeError:
        pass


if __name__ == '__main__':
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
