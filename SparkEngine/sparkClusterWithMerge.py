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
import numpy as np
import collections
from stemming.porter2 import stem

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

def updateTweetsCount(new_val, running_counts):
    return sum(new_val) + (running_counts or 0)

def updateStatesKws(new_features_stream, feature_count):
    
    with open('../data/staticwordcluster_new.txt', 'r') as wordcluster_text:
        word_cluster = json.load(wordcluster_text)

    if feature_count is None:
        feature_count = dict()
        for key in word_cluster:
            feature_count[key] = 0

    for new_features in new_features_stream:
        for feature in new_features:
            for key in word_cluster:
                if feature in word_cluster[key]:
                    feature_count[key] += 1
    
    return feature_count

def updateWordCluster(new_feature_pool, cluster):

    if cluster is None:
        with open('../data/staticwordcluster_new.txt', 'r') as wordcluster_text:
            word_cluster0 = json.load(wordcluster_text)
        d = collections.defaultdict(dict)
        cluster = [word_cluster0, d]

    word_cluster = cluster[0]
    candidate_cluster = cluster[1]
    keys = []
    for val in word_cluster.itervalues():
        keys = keys + val
    candidate_keys = candidate_cluster.keys()

    # update the candidate pool
    
    #if new_feature_pool != []:
    for new_features in new_feature_pool:
        for new_feature0 in new_features:
            new_feature = stem(new_feature0)
            if new_feature not in keys:
                if new_feature in candidate_keys:
                    candidate_cluster[new_feature]['count'] += 1 
                    for w in new_features:
                        w = stem(w)
                        for k,v in word_cluster.iteritems():
                            if w in v:
                                if k in candidate_cluster[new_feature].keys():
                                    candidate_cluster[new_feature][k] += 1
                                else:
                                    candidate_cluster[new_feature][k] = 1
                else:
                    candidate_cluster[new_feature]['count'] = 1 
                    for w in new_features:
                        w = stem(w)
                        for k,v in word_cluster.iteritems():
                            if w in v:
                                candidate_cluster[new_feature][k] = 1        
    
    # update the word pool
    delete_words = []
    for key, word in candidate_cluster.iteritems():
        count = word['count']
        fsum = sum([word[k] for k in word if k!='count'])
        if count > 100:
            if float(fsum)/count < 0.2:
                word_cluster[key] = key
                delete_words.append(key)
            else:
                word_temp = word
                del word_temp['count']
                maxc = max(word_temp)
                if float(word_temp[maxc])/count > 0.2:
                    word_cluster[maxc].append(key)
                    delete_words.append(key)
                
    # clear candidate pool
    for word in delete_words:
        del candidate_cluster[word]
    
    with open('../data/staticwordcluster_new.txt', 'w') as f:
        json.dump(word_cluster, f)
    
    newcluster = [word_cluster, candidate_cluster]

    return newcluster

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
    features = [x for x in features if x!='job' and x!='hire']

    return features

def getTopCluster(feature_count):
    return sorted(feature_count.items(), key=lambda x: x[1], reverse=True)

def getNewFeature(data):
    newfeatures = []
    for x in data:
        if x not in ['job']:
            newfeatures.append([x,data])
    return newfeatures

def getWordList(data):
    word_list = []
    for key, val in data.iteritems():
        word_list = word_list + val

    return word_list

if __name__ == '__main__':
    sc = SparkContext(appName="PythonTwitterStreaming")
    ssc = StreamingContext(sc, 1)
    tweetStream = KafkaUtils.createStream(ssc, 'localhost:2181', "kafka-stream-redis", {'tweets': 1})
    tweets = tweetStream.map(lambda x: x[1])

    ssc.checkpoint("./checkpoint-tweet")
    
    text = tweets.map(lambda x: json.loads(x)['text'] )
    geo = tweets.map(lambda x: json.loads(x)['geo'] )

    tweetscount = text.map(lambda x: ('counts', 1)).updateStateByKey(updateTweetsCount)

    features = text.map(lambda x: getFeature(x))
    feature_pool = features.map(lambda x: ('feature_pool', x)).window(20,20)
    word_cluster = feature_pool.updateStateByKey(updateWordCluster)

    statescounts = text.map(lambda x: (getState(x), getFeature(x)) ).window(5,5).reduceByKey(lambda x, y: x + y)
    stateskws = statescounts.updateStateByKey(updateStatesKws)
    statestop = stateskws.map(lambda x: (x[0], getTopCluster(x[1])))

    statestop.foreachRDD(lambda rdd: rdd.foreach(publishToRedis) )
    word_cluster.pprint()

    ssc.start()
    ssc.awaitTermination()
