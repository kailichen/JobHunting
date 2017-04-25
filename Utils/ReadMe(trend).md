### Please refer to the SampleOutput.txt

##### The attributes are: {Time, List of tweets count in every 5 seconds, probablity of tweets count going up in next 5 second, 1 represents up/ 0 represents down} 

##### For example,

```
2017-04-24 20:51:20,[3, 1, 2, 6, 1, 6, 1, 7, 0, 7, 0, 4, 1, 1, 6, 3, 3, 8, 2, 1],0.654605263158,1
```

#### To run the script

##### After start streaming,

```
$spark-submit trend.py
```
