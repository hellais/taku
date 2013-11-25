from datetime import datetime
from taku import counter

import unittest
test_tweet = Tweet(text="Questo è un tam-1 molto bello.",
                   date=datetime.now())

class TestCounter(unittest.TestCase):
    def setUp(self):
        from taku.models import Keyword
        from taku import db
        db.init()
        for i in range(10):
            keyword = Keyword()
            keyword.name = "Tam-"+str(i)
            keyword.words = "spam|ham|tam-"+str(i)
            db.session.add(keyword)
            db.session.commit()

    def test_count_keys(self):
        counter.count_keys(test_tweet)

    def test_compute_sentiment(self):
        from taku.models import Tweet, Keyword
        keyword = db.session.query(Keyword).filter_by(name="Tam-1").first()
        before_counter = int(keyword.counter.counter)
        before_counterpos = int(keyword.counter.counterpos)

        compute_sentiment(test_tweet, 'tam-1')

        keyword = db.session.query(Keyword).filter_by(name="Tam-1").first()
        assert keyword.counter.counter == (before_counter + 1)
        assert keyword.counter.positive == (before_counterpos + 1)

    def test_get_alternative_keys(self):
        from taku.counter import get_alternative_keys
        keyword = db.session.query(Keyword).filter_by(name="Tam-1").first()
        assert get_alternative_keys(keyword.words) == ['spam', 'ham', 'tam-1']

if __name__ == '__main__':
    unittest.main()
