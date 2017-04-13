# Stream Processing

### by Kaili Chen, Tingyu Mao, Yulong Qiao

### Framework
Kafka, Spark, Redis. 
** We use kafka to pull live data from twitter api and generate input stream data for spark engine. After data processing, we publish data to redis. 

### Installation
#### Kafka
There are three thing we need to prepare.
1. kafka_2.11-0.10.2.0, download from https://kafka.apache.org/downloads 
2. spark-streaming-kafka-0-8-assembly_2.11-2.1.0.jar, download from https://mvnrepository.com/artifact/org.apache.spark/spark-streaming-kafka-0-8-assembly_2.11/2.1.0. Here it should be noted that the version of .jar file must be consistent with the scala you use in spark. To check scala version, please start your spark-shell and open localhost:4040 on web browser to check. And the above-mentioned .jar belongs to scala2.11. And after download, put .jar file under /jar in spark directory.
3. pip install all require packages of python


#### start Kafka server
Go to the directory where you install kafka package and start "zookeeper" and "kafka server". Here are the commands.
Open your terminal,

```sh
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```

Open another terminal,

```sh
$ bin/kafka-server-start.sh config/server.properties
```

Now you have start kafka server. Then you need to create a topic like "tweets" for queuing
Open a new terminal and type in,

```sh
$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic tweets
```
Right now you have created a topic named ```tweets```

check the generated topics by, here 2181 is the default port kafka would use. You can change it by setting the config file.

```sh
$ bin/kafka-topics.sh --list --zookeeper localhost:2181
```

Then you can pull tweets to this port. 
```sh
$ python Streaming/tweetFetcher.py
```

To check the data you just pull in, open a new terminal and type in,
```sh
 $ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic tweets
```

Now you have finish the step to pull live data and then we go to how to process stream data in spark.

### Spark Engine
This is the core part of our work and so far I still choose to use pyspark and many libraries are available. Besides, I think it is necessary to understand the framework of spark, because, otherwise, we will make many programming mistakes here and debug in spark is annoying.
** Here are some useful links. 
http://spark.apache.org/docs/latest/streaming-programming-guide.html#output-operations-on-dstreams, http://spark.apache.org/docs/latest/cluster-overview.html 
1. Before running spark_engine.py, you need to open redis server and download page will be shown in next section.
2. Assure that the previous terminal are still active and then run spark engine
spark-submit sparkSubmit.py.
3. Now sparkSubmit.py send to tweet data to redis "twitterchannel" channel. And later we can send different data to different channels of redis. Besides, you can go to localhost:4040 to check running situation. So far, the spark_engine.py is just an empty core without functionality. And we need to add all our analytics tasks into it.

### Redis And Flask
You need to download redis and install redis-py python api.
1. download and install redis. Here is a useful link for Mac user. But you can try the latest version of redis.
http://yijiebuyi.com/blog/d8ab4b444c16f42cefe30df738a42518.html 
2. pip install redis

After installation,
3. start redis server.
4. run webapp.py -- python webapp.py. So far, it is also an empty app but if you open localhost:9999/stream in web browser, you will see the page keeps updating the tweets on job.

## Work plan
Now we have finish the whole set-up work and in the next days, we can divide into two parts. I hope @Yulong can polish the "webapp" part. And we need to do discuss more on what kinds of data should we presents on web. And I and @Kaili can focus on analysis. And the short-term goal for this week's presentation is that we can display the live job posting on geomap. Besides, to simplify the work of set-up, i.e, open redis or kafka, for mac user, it is recommended to write a shell script to make things easy.





