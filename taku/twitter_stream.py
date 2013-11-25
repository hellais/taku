from taku.settings import config
from taku.models import save_tweet

from twython import TwythonStreamer

class TakuStreamer(TwythonStreamer):
    def on_success(self, data):
        save_tweet(data)
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code

def monitor(keyword):
    stream = TakuStreamer(config.app_key, config.app_secret,
                          config.oauth_token, config.oauth_token_secret)
    stream.statuses.filter(track=keyword)
