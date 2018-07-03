import requests
import tornado.web

from wordcloud import WordCloud
from settings import WCLOUD_PATH
from utils.text import make_word_list, make_word_cloud


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')

    def post(self):
        url = self.request.arguments['url']
        if isinstance(url, list):
            url = url[0]
        url = url.decode('utf-8')

        r = requests.get(url)
        words = make_word_list(r.text)
        wcloud = make_word_cloud(words)
        self.write({'words': words, 'word_cloud': wcloud})
