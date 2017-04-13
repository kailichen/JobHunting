import sys
import json
import redis

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

def publishToRedis(tup):
    tweet = tup
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    r.publish("twitterchannel", tweet)

if __name__ == '__main__':
    sc = SparkContext(appName="PythonTwitterStreaming")
    ssc = StreamingContext(sc, 1)
    tweetStream = KafkaUtils.createStream(ssc, 'localhost:2181', "kafka-stream-redis", {'tweets': 1})
    tweets = tweetStream.map(lambda x: x[1])

    ssc.checkpoint("./checkpoint-tweet")
    tweets.foreachRDD(lambda rdd: rdd.foreach(publishToRedis))

    ssc.start()
    ssc.awaitTermination()
