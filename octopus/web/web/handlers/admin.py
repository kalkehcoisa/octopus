import tornado.web
from tornado import gen

from models import DBSession, UrlSentiment, WordUsage


class WordUsageHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        items = DBSession.query(WordUsage).order_by(WordUsage.count.desc())
        self.render(
            'admin.html',
            **{'items': items, 'title': 'Word Frequency'}
        )


class UrlSentimentHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        items = DBSession.query(UrlSentiment).order_by(UrlSentiment.url)
        self.render(
            'admin.html',
            **{'items': items, 'title': 'Url Sentiments'}
        )
