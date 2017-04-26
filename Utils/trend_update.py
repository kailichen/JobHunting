from __future__ import division
import sys
import json
import redis

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import googlemaps
import math

def publishToRedis(tup):
    tweet = tup
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    r.publish("twitterchannel", tweet)

    # rdd1 = str(rdd)
    # f = open("/Users/Kaili/Desktop/tweetTestTTT.txt", 'a')
    # f.write(rdd1)
    # f.write("\n")
    # f.close()

def updateFunction(new_value, old_value):
    return new_value - old_value

def get_clusetername(line):
    cluster_name = line.strip()

    if cluster_name == 'medical':
        output = 'Medical'
    elif cluster_name == 'technology':
        output = 'Technology'
    elif cluster_name == 'finance':
        output = 'Finance'
    else:
        output = 'Unknown'

    return (output, 1)

def saveFile(time, rdd):
    f = open("/Users/Kaili/Desktop/tweetCount.txt", 'a')
    f.write(str(time))
    f.write(str(rdd.collect()))
    f.write("\n")
    f.close()

def predict(rdd):

    count = str(rdd)

    l = []

    l.append(rdd[0][0][0][0])
    l.append(rdd[0][0][0][1])
    l.append(rdd[0][0][1])
    l.append(rdd[0][1])
    l.append(rdd[1])

    # tmp = count.replace("[", "")
    # tmp = tmp.replace("]", "")
    # tmp = tmp.replace(",", "")
    # clean = tmp.split(" ")
    # l = []
    # if clean[0] == '':
    #     for i in range(0, 5):
    #         l.append(0)
    # else:
    #     length = len(clean)
    #     for i in range(0, 5):
    #         if i < 5 - len(clean):
    #             l.append(0)
    #         else:
    #             l.append(int(clean[i - 5 + len(clean)]))

    # list: every 5 sec count
    list = []
    for i in range(0, 5):
        if i == 0:
            list.append(l[0])
        else:
            list.append(l[i] - l[i - 1])

    binary = []
    miu = (sum(list) - list[0])/4
    for i in range(1, 5):
        if list[i] > miu:
            binary.append(1)
        else:
            binary.append(0)
    if list[0] > miu:
        cur = 1
    else:
        cur = 0
    miu = sum(binary) / 4
    sd = 0
    for i in binary:
        sd = sd+(i-miu)*(i-miu)
    sd = math.sqrt(sd/4)/4

    if sd == 0:
        alpha = 25
    else:
        alpha = (((1-miu)/(sd*sd))-(1/miu))*(miu*miu)
    if miu == 0:
        beta = 25
    else:
        beta = alpha*((1/miu)-1)


    if cur == 1:
        alpha = alpha+1
    else:
        beta = beta+1
    mean_post = beta / (alpha + beta)
    sd_post = math.sqrt(alpha * beta / (((alpha + beta) * (alpha + beta)) * (alpha + beta + 1)))


    if mean_post >= 0.5:
        up = 1
    else:
        up = 0

    return "prob:" + str(mean_post) + "cur:" + str(list)


    #################################################################
    #                                                               #
    #  mean_post: probability of getting more jobs in the next 5 s  #
    #                                                               #
    #################################################################


if __name__ == '__main__':
    sc = SparkContext(appName="PythonTwitterStreaming")
    ssc = StreamingContext(sc, 5)
    tweetStream = KafkaUtils.createStream(ssc, 'localhost:2181', "kafka-stream-redis", {'tweets': 1})
    tweets = tweetStream.map(lambda x: x[1])

    ssc.checkpoint("./checkpoint-tweet")
    # tweets.foreachRDD(printlist)

    # counter = tweets.countByWindow(10, 2)
    # pairs = counter.map(lambda x: ("hello", int(x[0])))
    # pairs.updateStateByKey(updateFunction).foreachRDD(printlist)

    # window_length = 15
    # frequency = 6
    # lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    # window_counts = lines.map(get_clusetername).reduceByKeyAndWindow(addFunc, invAddFunc, window_length, frequency)
    # window_counts.pprint()

    # tweets.pprint()
    # tweets.count().pprint()

    ## --- Processing
    # a = sc.accumulator(0)
    # b = sc.accumulator(0)

    parsed = tweetStream.map(lambda v: json.loads(v[1]))

    # Count number of tweets in the batch
    # count_this_batch = tweetStream.count().map(lambda x: ('Tweets this batch: %s' % x))
    count_0 = tweetStream.count()

    # Count by windowed time period
    # count_windowed = tweetStream.countByWindow(60, 5).map(lambda x: ('Tweets total (One minute rolling count): %s' % x))
    count_1 = tweetStream.countByWindow(10, 5)
    count_2 = tweetStream.countByWindow(15, 5)
    count_3 = tweetStream.countByWindow(20, 5)
    count_4 = tweetStream.countByWindow(25, 5)
    # count_5 = tweetStream.countByWindow(30, 5)
    # count_6 = tweetStream.countByWindow(35, 5)
    # count_7 = tweetStream.countByWindow(40, 5)
    # count_8 = tweetStream.countByWindow(45, 5)
    # count_9 = tweetStream.countByWindow(50, 5)
    # count_10 = tweetStream.countByWindow(55, 5)
    # count_11 = tweetStream.countByWindow(60, 5)
    # count_12 = tweetStream.countByWindow(65, 5)
    # count_13 = tweetStream.countByWindow(70, 5)
    # count_14 = tweetStream.countByWindow(75, 5)
    # count_15 = tweetStream.countByWindow(80, 5)
    # count_16 = tweetStream.countByWindow(85, 5)
    # count_17 = tweetStream.countByWindow(90, 5)
    # count_18 = tweetStream.countByWindow(95, 5)
    # count_19 = tweetStream.countByWindow(100, 5)

    # Get authors
    authors_dstream = parsed.map(lambda tweet: tweet['user']['screen_name'])

    # Count each value and number of occurences
    count_values_this_batch = authors_dstream.countByValue() \
        .transform(lambda rdd: rdd \
                   .sortBy(lambda x: -x[1])) \
        .map(lambda x: "Author counts this batch:\tValue %s\tCount %s" % (x[0], x[1]))

    # Count each value and number of occurences in the batch windowed
    count_values_windowed = authors_dstream.countByValueAndWindow(60, 5) \
        .transform(lambda rdd: rdd \
                   .sortBy(lambda x: -x[1])) \
        .map(lambda x: "Author counts (One minute rolling):\tValue %s\tCount %s" % (x[0], x[1]))

    # Write total tweet counts to stdout
    # Done with a union here instead of two separate pprint statements just to make it cleaner to display
    # count_this_batch.union(count_windowed).foreachRDD(saveFile)
    pair0=count_0.map(lambda x: ("hello", x))
    pair1=count_1.map(lambda x: ("hello", x))
    pair2=count_2.map(lambda x: ("hello", x))
    pair3=count_3.map(lambda x: ("hello", x))
    pair4=count_4.map(lambda x: ("hello", x))
    # count_0.union(count_1).union(count_2).union(count_3).union(count_4).union(count_5).union(count_6).union(count_7).union(count_8). \
    #     union(count_9).union(count_10).union(count_11).union(count_12).union(count_13).union(count_14).union(count_15). \
    #     union(count_16).union(count_17).union(count_18).union(count_19).foreachRDD(predict)
    # newrdd = count_0.union(count_1).union(count_2).union(count_3).union(count_4).map(lambda x: predict(x))
    newrdd = pair0.join(pair1).join(pair2).join(pair3).join(pair4).map(lambda x: predict(x[1]))
    # newrdd.pprint()
    newrdd.foreachRDD(lambda rdd: rdd.foreach(publishToRedis))


    # Write tweet author counts to stdout
    # count_values_this_batch.pprint(5)
    # count_values_windowed.pprint(5)


    ssc.start()
    ssc.awaitTermination()