#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import logging
from random import getrandbits
import sys
import urllib2

from bs4 import BeautifulSoup as BS
from telebot import types
import telebot

reload(sys)
sys.setdefaultencoding("utf-8")

# Log
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('qgis_bot.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

# Config
TOKEN = ''
url_q = 'http://plugins.qgis.org/search/?q={0}'
url_p = 'http://plugins.qgis.org/'
parser = "html.parser"

# Start
bot = telebot.TeleBot(TOKEN)

re_plugins = {}


# Funtions
def main():
    bot.polling(none_stop=True)


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    photo = open('images/botfather.png', 'rb')
    bot.send_message(cid,
                     "Welcome to QGIS search Plugins bot !!!! Let's start looking for plugins")
    bot.send_photo(cid, photo)


@bot.inline_handler(func=lambda query: True)
def inline(query):

    query_v = query.query

    if not query_v:
        return

    r = list()

    try:
        plugins = get_result(query_v)
    except Exception as e:
        logger.exception(str(e))

    try:
        if not plugins:
            r.append(types.InlineQueryResultArticle(
                        id=hex(getrandbits(64))[2:],
                        title="Oooops!!No results",
                        description="Try using other text.",
                        input_message_content=types.InputTextMessageContent(
                                message_text="Oooops!!No results"
                        ),
                        thumb_url="https://goo.gl/sJMSCH",
                        thumb_width=12,
                        thumb_height=12
                        ))

        else:
            for key, value in plugins.iteritems():
                url = url_p + value
                r.append(types.InlineQueryResultArticle(
                        id=hex(getrandbits(64))[2:],
                        title=key,
                        input_message_content=types.InputTextMessageContent(
                                message_text=url
                        ),
                        url=url,
                        thumb_url="https://goo.gl/AW5cRD",
                        thumb_width=12,
                        thumb_height=12
                        ))

        bot.answer_inline_query(query.id, r, cache_time=1)

    except Exception as e:
        logger.exception(str(e))


def get_result(query_string):
    sanitize_q = '+'.join(query_string.split())

    page = url_q.format(sanitize_q)
    content = urllib2.urlopen(page).read()
    soup = BS(content, parser)
    re_plugins = {}
    for p in soup.findAll("p", {"class": "search-item"}):
        link = p.contents[1].attrs['href']
        text = p.text
        re_plugins[text] = link

    return re_plugins


if __name__ == '__main__':
    main()
