import hashlib
import uuid

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers

import settings

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
session_fac = sessionmaker()
session_fac.configure(bind=engine)

Base = declarative_base()

DBSession = session_fac()


class WordUsage(Base):
    __tablename__ = 'word_usage'

    id = Column(String(length=255), primary_key=True)
    # no asymmetrical encryption: how can I show the data in the "admin"?
    word = Column(String(length=255), nullable=False, unique=True)
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
    __tablename__ = 'surl_entiment'

    id = Column(String(length=255), primary_key=True)
    # no asymmetrical encryption: how can I show the data in the "admin"?
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
