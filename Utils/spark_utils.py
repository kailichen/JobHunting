import re
import redis
import json
#from pymongo import MongoClient
import googlemaps

state_list=["AL","AK","AZ","AR", "CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
with open('../AppCreds/TwitterAcct.json','r') as config_data:
    googlemaps_key = json.load(config_data)['googlemaps_key']

def sendToRedis(tup):
    word   = tup
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    r.publish("twitterchannel", word)
    #print('h'*40)
    #print(word)

# send geo info to redis
def RedisGeoChannel(geotext):
    tweet = geotext[0]
    geo = geotext[1]
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    r.publish("tweetgeochannel", [tweet,geo])

    print('h'*40)
    print(tweet)

def test(tup):
    print(tup)

# for counting the most common words
def updateFunc(new_values, last_sum):
    return sum(new_values) + (last_sum or 0)

# get geo info
def getGeo(tweet):
    geo = dict()
    pattern = re.compile(r'\W+')
    words = pattern.split(tweet)
    gmaps = googlemaps.Client(key = googlemaps_key)
    for i in range(0,len(words)):
        if words[i] in state_list:
            state = str(words[i])
            city = str(words[i-1])
            for x in range(2, 4):
                location = city + ", " + state
                result = gmaps.geocode(location)
                if result:
                    geo['geo'] = result[0]['geometry']['location']
                    return geo
                else:
                    city = str(words[i-x]) + " " + city

    return geo
