import sys
import json
import re
import redis
import time

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

def publishToRedis(tup):
    tweet = tup
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    r.publish("twitterchannel", tweet)
    print('#'*40)
    #print('time: ', time.time())
    print(tweet)

def saveToFile(time, rdd):
    f = open('../data/countsState.txt', 'a')
    f.write( str(time)+','+str(rdd.collect()) )
    f.write('\n')
    f.close()
    print(rdd.collect())

def updatediff(new_val, old_val):
    if old_val is None:
        old_val = 0
    return sum(new_val)-old_val

def updateStates(new_val, old_val):
    if old_val is None:
        old_val = 0
    return sum(new_val) + old_val

def getState(tweet):
    state_list=["AL","AK","AZ","AR", "CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
    pattern = re.compile(r'\W+')
    words = pattern.split(tweet)
    state = 'null'
    for i in range(0,len(words)):
        if words[i] in state_list:
            state = str(words[i])
    return state


if __name__ == '__main__':
    sc = SparkContext(appName="PythonTwitterStreaming")
    ssc = StreamingContext(sc, 1)
    tweetStream = KafkaUtils.createStream(ssc, 'localhost:2181', "kafka-stream-redis", {'tweets': 1})
    tweets = tweetStream.map(lambda x: x[1])

    ssc.checkpoint("./checkpoint-tweet")
    
    text = tweets.map(lambda x: json.loads(x)['text'] )
    geo = tweets.map(lambda x: json.loads(x)['geo'] )

    statescounts = text.map(lambda x: (getState(x), 1) ).window(10,10).reduceByKey(lambda x, y: x + y)
    #stateschnls = statescounts.updateStateByKey(updateStates)
    #counts = text.countByWindow(5, 5)
    #pairs = counts.map(lambda x: ('hello', x))
    #windowedWordCounts = pairs.reduceByKeyAndWindow(lambda x, y: x + y, lambda x, y: x - y, 30, 10)
    #diff = pairs.updateStateByKey(updatediff)

    #diff.foreachRDD(lambda rdd: rdd.foreach(publishToRedis))
    #diffandcounts = diff.join(pairs)
    statescounts.foreachRDD(saveToFile)
    #diffandcounts.foreachRDD(lambda rdd: rdd.foreach(publishToRedis))
    #windowedWordCounts.foreachRDD(lambda rdd: rdd.foreach(publishToRedis))

    ssc.start()
    ssc.awaitTermination()
