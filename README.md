# Large Scale Stream Processing - Job Hunting in Twitter Streaming

## Team KTY: Kaili Chen, Tingyu Mao, Yulong Qiao

### Framework

- Apache **Kafka** as message queue
- Apache **Spark** as backend data analysis tool
- **Redis** as memcaching to enhance real-timeness
- **Flask** as framework for WebApp

### Architecture
![show architecture](https://cldup.com/qoPbmkcl9t.png)

### Installation
Our App requires proper installation of **Kafka**, **Spark**, and **Redis**.

#### Kafka
To install Kafka,

First, Check ```Scala``` version, run:

```sh
$ spark-shell
```

Then open ```localhost:4040``` to check ```scala``` version
![show scala version](https://cldup.com/9KM9Z3gsp9.png)
This pictures show scala version of 2.11

Installation: 

1. Download [kafka_2.11-0.10.2.0]

2. Download [spark-streaming-kafka-0-8-assembly_2.11-2.1.0.jar] and put into spark's ```jar``` directory.
  - Note that the version of .jar file must be consistent with the scala you use in spark. 

#### Redis

Easy Installation:

```sh
brew install redis
```

You can also turn to manual installation:

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

### App and System Service

#### We construct three apps
- Real-time job plotting on Google Map
  - spark-job: ```JobPlotting.py```
  - WebApp: ```WebApp_JobPlotting/```

- Real-time job Cluster by states of US
  - spark-job: ```JobCluster.py```
  - WebApp: ```WebApp_JobClusterAndTrend/```
  
- Real-time job Trending in US
  - spark-job: ```JobTrend.py```
  - WebApp: ```WebApp_JobClusterAndTrend/```

#### System Service
1. start kafka
2. start redis
3. submit spark job
4. start streaming
4. start WebApp
5. go to localhost and observe the app


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

#### Submit Spark Job

```sh
spark-submit JobPlotting.py (JobCluster.py JobTrend.py)
```
Now sparkSubmit.py send to tweet data to redis channel

#### start Streaming

```sh
python tweetFetcher.py
```

#### start Flask

```sh
python application.py (in WebApp_JobPlotting/ or WebApp_JobClusterAndTrend/)
```

### WebApp Demo

#### Real-time Job Plotting

![Job Plotting 1](https://cldup.com/aMp_SqjYMe.png)
Start the WebApp, job posts on Twitter is plotted on GoogleMap in real-time.
![Job Plotting 2](https://cldup.com/y27QA7Dj5W.png)
Click on the marker to Toggle job infomation

#### Real-time job Clustering
We utilize job clustering with SVG map. 
Start the WebApp, jobs clustered within each state will shown on the map. Hover onto each state to toggle.
![Job Cluster 1](https://cldup.com/3prpkE4DfT.png)
![Job Cluster 2](https://cldup.com/u5sGZSo1Xg.png)

#### Real-time job Trending
We utilize job trending with SVG map.
Start the WebApp, the map of US will change to different color
- ```Red``` means pessimistic
- ```Green``` means optimistic
- ```Yellow``` means no difference
![Job Trending 1](https://cldup.com/Ro0O8FHQhq.png)
![Job Trending 2](https://cldup.com/-Ahzd8eLf6.png)

## Future Work
Now we have finish the whole set-up work and in the next days, we can divide into two parts. I hope @Yulong can polish the "webapp" part. And we need to do discuss more on what kinds of data should we presents on web. And I and @Kaili can focus on analysis. And the short-term goal for this week's presentation is that we can display the live job posting on geomap. Besides, to simplify the work of set-up, i.e, open redis or kafka, for mac user, it is recommended to write a shell script to make things easy.





[kafka_2.11-0.10.2.0]:<https://kafka.apache.org/downloads>
[spark-streaming-kafka-0-8-assembly_2.11-2.1.0.jar]:<https://mvnrepository.com/artifact/org.apache.spark/spark-streaming-kafka-0-8-assembly_2.11/2.1.0>
[Redis 3.2]:<https://redis.io/download>
[Arch]:<https://github.com/kailichen/StreamProcessing/blob/master/resources/architecture.png>
