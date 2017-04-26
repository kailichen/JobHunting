import sys
import json
import re
import redis
import time

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from stemming.porter2 import stem
import operator

def publishToRedis(tup):
    state = tup[0]
    sortedcluster = tup[1]

    data = dict()
    data[state] = sortedcluster
    
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    r.publish("twitterchannel", json.dumps(data))
    print('#'*40)
    #print('time: ', time.time())
    print(data)

def saveToFile(rdd):
    f = open('../data/countsState3.txt', 'a')
    f.write( str(rdd) )
    f.write('\n')
    f.close()
    print(rdd)


def updateStatesKws(new_features, feature_count):
    
    with open('../data/staticwordcluster.txt', 'r') as wordcluster_text:
        word_cluster = json.load(wordcluster_text)

    if feature_count is None:
        feature_count = dict()
        for key in word_cluster:
            feature_count[key] = 0

    if new_features != []:
        for feature in new_features[0]:
            for key in word_cluster:
                if feature in word_cluster[key]:
                    feature_count[key] += 1
    
    return feature_count

def getState(tweet):
    state_list=["AL","AK","AZ","AR", "CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
    pattern = re.compile(r'\W+')
    words = pattern.split(tweet)
    state = 'null'
    for i in range(0,len(words)):
        if words[i] in state_list:
            state = str(words[i])
    return state

def getFeature(tweet):
    text= tweet
    url_texts = text.split('http')[1:]
    for url_text in url_texts:
        url = 'http' + url_text.split(' ')[0]
        text = text.replace(url, '')

    state_list=["AL","AK","AZ","AR", "CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
    pattern = re.compile(r'\W+')
    words = pattern.split(text)
    for i in range(0,len(words)):
        if words[i] in state_list:
            state = words[i]
            city = words[i-1]
            location = city + ", " + state
            geo = location
            text = text.replace(geo, '')

    line = text.split(None)
    wordsline = [''.join(pattern.split(x)).lower() for x in line if x.startswith('#')]
    features = [stem(x) for x in wordsline if x!='']

    return features

def getTopCluster(feature_count):
    return sorted(feature_count.items(), key=lambda x: x[1], reverse=True)

if __name__ == '__main__':
    sc = SparkContext(appName="PythonTwitterStreaming")
    ssc = StreamingContext(sc, 1)
    tweetStream = KafkaUtils.createStream(ssc, 'localhost:2181', "kafka-stream-redis", {'tweets': 1})
    tweets = tweetStream.map(lambda x: x[1])

    ssc.checkpoint("./checkpoint-tweet")
    
    text = tweets.map(lambda x: json.loads(x)['text'] )
    geo = tweets.map(lambda x: json.loads(x)['geo'] )

    statescounts = text.map(lambda x: (getState(x), getFeature(x)) ).window(10,10).reduceByKey(lambda x, y: x + y)
    stateskws = statescounts.updateStateByKey(updateStatesKws)
    statestop = stateskws.map(lambda x: (x[0], getTopCluster(x[1])))

    statestop.foreachRDD(lambda rdd: rdd.foreach(publishToRedis) )

    ssc.start()
    ssc.awaitTermination()
