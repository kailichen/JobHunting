import googlemaps

state_list=["AL","AK","AZ","AR", "CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

def main():
    var = raw_input("Please enter tweet: ")
    location = getGeo(var)
    print location

def getGeo(tweet):
    words = tweet.split()
    for i in range(0,len(words)):
        if words[i] in state_list:
            state = str(words[i])
            city = str(words[i-1])
            city = city.replace(",","")
            for x in range(2, 4):
                location = city + ", " + state
                gmaps = googlemaps.Client(key='AIzaSyBDj0j93g11NpN7qEEvnmFaQlQVponAAqs')
                result = gmaps.geocode(location)
                if result:
                    return result
                else:
                    city = str(words[i-x]) + " " + city

if __name__ == "__main__":
    main()