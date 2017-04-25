"""
Team KTY for final project of ELEN 6889 Large Scale Stream Processing
@description: tweetFetcher.py call Twitter APIs to fetch tweets, perform validation then send to Apache Kafka
@param: None
@return: None
"""
import os
import sys
import json
import tweepy

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener
from tweepy import API
from time import sleep

from kafka import SimpleProducer, KafkaClient

"""reload intepretor, add credential path"""
reload(sys)
sys.setdefaultencoding('UTF8')
sys.path.append('../Utils')

from spark_utils import getGeo

"""import credentials from root/AppCreds"""
with open(os.path.dirname(sys.path[0])+'/AppCreds/TwitterAcct.json','r') as TwitterAcct:
    twittconf = json.loads(TwitterAcct.read())
consumer_key = twittconf["consumer_key"]
consumer_secret = twittconf["consumer_secret"]
access_token = twittconf["access_token"]
access_token_secret = twittconf["access_token_secret"]


"""Kafka Settings"""
TOPIC = b'tweets'
KAFKA_CLIENT = KafkaClient('localhost:9092')
KAFKA_PRODUCER = SimpleProducer(KAFKA_CLIENT)

"""streaming model"""
class TweetStreamListener(StreamListener):
    def __init__(self, api):
        # api is not yet implemented
        self.topic = TOPIC
        self.api = api
        super(StreamListener, self).__init__()
        self.producer = KAFKA_PRODUCER
        # backoff time when reaches status==420 AKA reach speed limit
        self.backoff = 1
        self.count = 1
    
    def on_data(self, data):
        tweetJson = json.loads(data.encode('utf8'))
        # print tweetJson
        # print tweetJson['place'] is None
        # strict definition to avoid key error
        try:
            if 'place' in tweetJson:
                if ('lang' in tweetJson):
                    if tweetJson['place'] is not None:
                        if (tweetJson['place']['country_code'] == 'US') & (tweetJson['lang'] == 'en'):

                            print ('fetching No. '+ str(self.count) +' Tweet')

                            data_url = tweetJson['entities']['urls'][0]['url']
                            data_text = tweetJson['text']
                            data_geo = None#getGeo(data_text)
                            if not data_geo:
                                print('*'*80)
                                print('geo not in text, use geo_tag instead')
                                print('*'*80)
                                data_geo = tweetJson['geo']

                            senddata = {}
                            senddata['url'] = data_url
                            senddata['text'] = data_text
                            senddata['geo'] = data_geo
                            
                            #print ('fetching No. '+ str(self.count) +' Tweet')
                            self.backoff /= 2
                            self.count += 1
                            self.producer.send_messages(self.topic, json.dumps(senddata).encode('utf8'))
                        
        except Exception as error:
            print "kafka raise exception, printing out traceback..."
            print error
            return True
        return True

    def on_error(self, status):
        if status == 420:
            sleep(self.backoff)
            # exponentially raise up backoff time to get out of 420
            self.backoff *= 2
        return True;

    def on_timeout(self):
        return True 

"""streaming process"""
def streaming():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    stream = tweepy.Stream(auth, listener = TweetStreamListener(api))
    stream.filter(track=['job'], languages = ['en'])

"""main module"""
if __name__ == '__main__':
    print ('Twitter streaming begins')
    streaming()
