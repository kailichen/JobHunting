# Large Scale Stream Processing

## Team KTY: Kaili Chen, Tingyu Mao, Yulong Qiao

### Framework
- Apache **Kafka** as queuing service
- Apache **Spark** as data analysis tool
- **Redis** as in-memory caching to enhance real-timeness
- **Flask** as web framework in Python

### Architecture
![alt text](https://cldup.com/qoPbmkcl9t.png)
### Installation

#### Kafka

Check ```Scala``` version, run:
```sh
$ spark-shell
```

Then open ```localhost:4040``` to check

Installation: 

1. Download [kafka_2.11-0.10.2.0]

2. Download [spark-streaming-kafka-0-8-assembly_2.11-2.1.0.jar]
  - Note that the version of .jar file must be consistent with the scala you use in spark. 

#### Redis

Easy Installation:

```sh
brew install redis
```

Installation:

1. Download [Redis 3.2]

2. Make, test and Install
```sh
$ cd redis-3.2.8
$ sudo make
$ sudo make test
$ sudo make install
```
3. Revise ```conf``` file

```sh
$ cd redis-3.2.8
```

Find ```redis.conf```, open it by ```vim```, revise the line of ```dir.``` as ```dir /opt/redis/```

4. mkdir in /opt/ and move redis.conf to /etc, and you are done

```sh
$ mkdir /opt/redis
$ mv redis.conf /etc
```

### Start Service

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

#### start Redis server

```sh
/usr/local/bin/redis-server /etc/redis.conf
```

#### start Spark server

```sh
spark-submit sparkSubmit.py
```
Now sparkSubmit.py send to tweet data to redis "twitterchannel" channel

#### start Streaming

```sh
python tweetFetcher.py
```

#### start Flask

```sh
python application.py
```
## Work plan
Now we have finish the whole set-up work and in the next days, we can divide into two parts. I hope @Yulong can polish the "webapp" part. And we need to do discuss more on what kinds of data should we presents on web. And I and @Kaili can focus on analysis. And the short-term goal for this week's presentation is that we can display the live job posting on geomap. Besides, to simplify the work of set-up, i.e, open redis or kafka, for mac user, it is recommended to write a shell script to make things easy.





[kafka_2.11-0.10.2.0]:<https://kafka.apache.org/downloads>
[spark-streaming-kafka-0-8-assembly_2.11-2.1.0.jar]:<https://mvnrepository.com/artifact/org.apache.spark/spark-streaming-kafka-0-8-assembly_2.11/2.1.0.>
[Redis 3.2]:<https://redis.io/download>
[Arch]:<https://github.com/kailichen/StreamProcessing/blob/master/resources/architecture.png>
