from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base                                     

engine = create_engine('sqlite:///testing.sqlite', echo=True)
Base = declarative_base(bind=engine)
session = scoped_session(sessionmaker(engine))

Base.query = session.query_property()
def init():
    from taku.models import Tweet, KeywordCounter, Keyword
    Base.metadata.create_all(bind=engine)
