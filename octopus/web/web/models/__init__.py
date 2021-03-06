import hashlib
import uuid

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers

import settings
from models import types

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()

engine = create_engine(
    "mysql://{user}:{passwd}@octopus_db_1/{dbname}".format(
        dbname=settings.DB_NAME,
        passwd=settings.DB_PASSWORD,
        user=settings.DB_USER,
    ),
    encoding='utf-8',
    echo=True
)
session_fac = sessionmaker(autoflush=False)
session_fac.configure(bind=engine)

Base = declarative_base()

DBSession = session_fac()


class WordUsage(Base):
    """
    Model that stores the global statistics about word usage
    in the analyzed websites.
    It keeps the words and their usage count.
    """
    __tablename__ = 'word_usage'

    id = Column(String(length=255), primary_key=True)
    word = Column(types.RsaString, nullable=False)
    count = Column(Integer, nullable=False)

    def __init__(self, word, count):
        self.word = word
        self.count = count

        self.id = hashlib.sha512((word + uuid.uuid4().hex).encode()).hexdigest()

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'count': self.count,
        }


class UrlSentiment(Base):
    """
    This model keeps the data about the sentiment expressed
    by the url contents.
    """
    __tablename__ = 'url_sentiment'

    id = Column(String(length=255), primary_key=True)
    url = Column(String(length=255), nullable=False, unique=True)
    sentiment = Column(String(length=255), nullable=False)

    def __init__(self, url, sentiment):
        self.url = url
        self.sentiment = sentiment

        self.id = hashlib.sha512((url + uuid.uuid4().hex).encode()).hexdigest()

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'sentiment': self.sentiment,
        }
