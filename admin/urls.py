from tornado.web import url

from .handlers import AdminWordListHandler


admin_urls = [
    url(r"^/admin/$", AdminWordListHandler, name='admin_word_list'),
]
