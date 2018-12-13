from tornado.web import url

from .handlers import WordCounterHandler


word_counter_urls = [
    url(r"^/word_counter/$", WordCounterHandler, name='word_counter'),
]
