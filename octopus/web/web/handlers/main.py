import json
import urllib.parse

import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from models import DBSession, UrlSentiment, WordUsage
from settings import WIT_AUTH_KEY
from utils.text import make_word_cloud, nltk_text, remove_tags


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def save_word_data(self, most_common):
        # saves the word data into the database
        objs = []
        for word, num in most_common:
            w_obj = DBSession.query(WordUsage).filter(WordUsage.word == word)
            if w_obj.count() > 0:
                w_obj = w_obj.first()
                w_obj.count += num
                DBSession.merge(w_obj)
            else:
                w_obj = WordUsage(word=word, count=num)
                objs.append(w_obj)

        if len(objs) > 0:
            DBSession.bulk_save_objects(objs)
            DBSession.flush()
            DBSession.commit()

        raise gen.Return(False)

    @gen.coroutine
    def sentiment_data(self, url, common_list):
        # do the sentiment analysis with wit.ai
        # saves the sentiment data into the database
        query_str = urllib.parse.quote_plus(
            ' '.join(common_list)[:280]
        )
        http_client = AsyncHTTPClient()
        r = yield http_client.fetch(
            'https://api.wit.ai/message?v=20180703&q={}'.format(query_str),
            headers={
                'Authorization': 'Bearer {WIT_AUTH_KEY}'.format(
                    WIT_AUTH_KEY=WIT_AUTH_KEY
                )
            })
        ents = json.loads(r.body)['entities']
        sentiment = ents and ents.get('sentiment')
        if sentiment:
            sentiment = sentiment[0]['value']
            s_obj = DBSession.query(UrlSentiment).filter(UrlSentiment.sentiment == sentiment)
            if s_obj.count() == 0:
                s_obj = UrlSentiment(url=url, sentiment=sentiment)
                DBSession.add(s_obj)
                DBSession.commit()

                raise gen.Return(s_obj)
        raise gen.Return(False)

    @gen.coroutine
    def get(self):
        self.render('index.html', page='home')

    @gen.coroutine
    def post(self):
        url = self.request.arguments['url']
        if isinstance(url, list):
            url = url[0]
        url = url.decode('utf-8')

        # gets the url contents, generates the words list
        # and the word_cloud
        http_client = AsyncHTTPClient()
        r = yield http_client.fetch(url)
        dirty_text = remove_tags(r.body)
        words = nltk_text(dirty_text)
        most_common, wcloud = make_word_cloud(words)
        common_list = list(dict(most_common).keys())
        self.write({'words': common_list, 'word_cloud': wcloud})
        self.flush()

        # saves the word data into the database
        yield self.save_word_data(most_common)

        # do the sentiment analysis with wit.ai
        # saves the sentiment data into the database
        yield self.sentiment_data(url, common_list)
