from datetime import datetime

from taku.db import Base, session
from taku.log import logger

class Keyword(Base):
    __tablename__ = "keyword"

    from sqlalchemy.orm import relationship
    from sqlalchemy import Column, Integer, String, ForeignKey

    id = Column(Integer, primary_key=True)
    words = Column(String())
    name = Column(String())

class KeywordCounter(Base):
    __tablename__ = "counter"

    from sqlalchemy.orm import relationship
    from sqlalchemy import Column, Integer, String, ForeignKey
    
    id = Column(Integer, primary_key=True)
    screen_name = Column(String())
    description = Column(String())

    keyword_id = Column(Integer)
    keyword = Column(Integer, ForeignKey('keyword.id'))

class Tweet(Base):
    __tablename__ = "tweet"

    from sqlalchemy.orm import relationship
    from sqlalchemy import Column, Integer, String, Date

    id = Column(Integer, primary_key=True)
    date = Column(Date, primary_key=True)
    text = Column(String(256))
    user_id = Column(Integer)
    retweet_count = Column(Integer)

    def __str__(self):
        return "<Tweet (text=%r)>" % self.text

def save_tweet(data):
    from sqlalchemy.exc import IntegrityError

    tweet = Tweet()
    tweet.id = int(data['id'])
    tweet.text = data['text']
    tweet.retweet_count = int(data['retweet_count'])
    tweet.date = datetime.strptime(data['created_at'],
                                   "%a %b %d %H:%M:%S +0000 %Y")
    
    try:
        session.add(tweet)
        session.commit()
    except IntegrityError:
        logger.error("Error in adding tweet %r" % tweet, exc_info=True)
        session.rollback()
    return tweet
