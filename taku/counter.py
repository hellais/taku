import re, logging

from taku.db import session
from taku.models import Keyword

from gazzatweet.utils import normalize
# import gazzatweet.configuration as conf
 
# import textlearn.saverloader
 
# keywords = dbmanager.get_keywords()


# subjectivityClassifier = textlearn.saverloader.load(conf.classifiers_path + 'subjectivity.textclassifier')
# polarityClassifier = textlearn.saverloader.load(conf.classifiers_path + 'polarity.textclassifier')

def get_alternative_keys(words_string, separator="|"):
    """
    Takes as input a word string and a separator. Outputs the normalized
    keywords.
    """
    return [utils.normalize(key) for key in keywords.word.split(ALT_SEP)]

def write_sentiment(tweet, keyword):
    """
    Calculates the sentiment of the tweet given as input and writes the
    appropriate values in the keyword table.
    """
    is_subjective = subjectivityClassifier.predict(tweet.text)

    if is_subjective and polarityClassifier.predict(tweet.text):
        keyword.counter.counterpos = keyword.counter.counterpos + 1
    elif is_subjective:
        keyword.counter.counterneg = keyword.counter.counterneg + 1

def count_keys(tweet):
    tokenize = lambda s : re.findall(r'\w+\'?', s, flags=re.UNICODE)

    keywords = session.query(Keyword).all()

    for keyword in keywords:
        alternative_keys = get_alternative_keys(keywords.words)
        if any([key in tokenize(normalize(tweet.text))
                for key in alternative_keys]):
            keyword.counter.counter = keyword.counter.counter + 1
            try:
                write_sentiment(tweet)
            except (UnicodeDecodeError, UnicodeEncodeError):
                logger.warning("A tweet was not UTF8-encoded correctly.", exc_info=True)
            session.commit()
