

from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient

import datetime
stop_time = datetime.datetime.now() + datetime.timedelta(hours=5)


MONGO_HOST= 'mongodb://localhost/Event'

#WORDS = ['#bigdata', '#AI', '#datascience', '#machinelearning', '#ml', '#iot']


CONSUMER_KEY = "KRcmUqbYaT6bC3lRxZbFyP76K"
CONSUMER_SECRET = "NVWLuCjq4h0tS2xFhNfEVh0kijRQkwIXZ7iZGLAdByc7TZpdmx"
ACCESS_TOKEN = "917327613009346561-wAu4RVeOukwW9XL9jUYe6OH0Ds0KcbM"
ACCESS_TOKEN_SECRET = "LWkxtMXdMBxiljxNbbMlD1JNPrAA3qtAsXx901f6KTPfC"

class StreamListener(tweepy.StreamListener):    
    #This is a class provided by tweepy to access the Twitter Streaming API. 

	def on_connect(self):
        # Called initially to connect to the Streaming API
		print("You are now connected to the streaming API.")
 
	def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
		print('An Error has occured: ' + repr(status_code))
		return False
 
	def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        
		if datetime.datetime.now() > stop_time:
			exit()
	    
		client = MongoClient(MONGO_HOST)
            
            # Use twitterdb database. If it doesn't exist, it will be created.
		db = client.Event
    
            # Decode the JSON from Twitter
		datajson = json.loads(data)
            
            #grab the 'created_at' data from the Tweet to use for display
		created_at = datajson['created_at']

            #print out a message to the screen that we have collected a tweet
		print("Tweet collected at " + str(created_at))
            
            #insert the data into the mongoDB into a collection called twitter_search
            #if twitter_search doesn't exist, it will be created.
		db.data.insert(datajson)
        

paths = 'keywords.txt'
while 1:
	try:
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
		#Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
		listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
		streamer = tweepy.Stream(auth=auth, listener=listener)
		#print("Tracking: " + str(WORDS))
		streamer.filter(track=open(paths,'r'))
	except:
		continue