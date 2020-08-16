"""
    API Key: BnB7ELEIRhNfqLVnyyHHHtb3t
    API Secret Key: pKUTbac4XualkRFdvFzDe8ZgAzbzYVlhV4SgIGLMMdGcNCUrgh
    Bearer Token: AAAAAAAAAAAAAAAAAAAAAGNbGwEAAAAAZchtYnm0wjpSCF%2FpdzyyB0bFxls%3Dm3crwWYx5oJsgjU2W23Dscyk285mL9C5sO1Nk3qCI4RlsNtA9O
	Access Token: '4713529994-QO1Z90HHs3gzgRdVlQuLPzL3T10cyxQTkPRBIs6'
	Access Token Secret: '6smcGs7lPElftGzmqOWGcPsr0CXdchuKqjJTcOLuDNJ0g'
 
"""
    
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from tweepy import Stream
from tweepy.streaming import Stream
from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Cursor
import TwitterKeyHandles

class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(TwitterKeyHandles.get_api_key, TwitterKeyHandles.get_api_secret_key)
        auth.set_access_token(TwitterKeyHandles.get_access_token, TwitterKeyHandles.get_access_token_secret)
        return auth

# # # TWITTER STREAMER # # #
class TwitterStreamer():
	"""
	Class for streaming and processing live tweets
	"""
	def __init__(self):
		self.twitter_authenticator = TwitterAuthenticator()

	def stream_tweets(self, fetched_tweets_filename, hashtag_list):
        # This handles twitter authentiation and connction to the Twitter streaming API
		listener = TwitterListner(fetched_tweets_filename)
		auth = self.twitter_authenticator.authenticate_twitter_app()
		stream = Stream(auth, listener)
		# This line filters Twitter streams to capture data by keywords
		stream.filter(track=hashtag_list)
    	  

# # # TWITTER STREAMER LISTNER # # #
class TwitterListner(StreamListener):
	"""
	This is a basic listener calss that just prints received ouputs to stdout.
	"""
 
	def __init__(self, fetched_tweets_filename):
		self.fetched_tweets_filename = fetched_tweets_filename
  
	def on_data(self, data):
		try:
			print(data)
			with open(self.fetched_tweets_filename, 'a') as tf:
				tf.write(data)
			return True
		except BaseException as e:
			print("Error on Data: %s " % str(e))
		return True
    
	def on_error(self, status):
		print(status)

if __name__ == "__main__":
    
	hashtag_list = ["Sushant Singh Rajput", "SSR", "MSD", "Mahendra Singh Dhoni"]
	fetched_tweets_filename = "tweets.json"
 
	twitter_streamer = TwitterStreamer()
	twitter_streamer.stream_tweets(fetched_tweets_filename, hashtag_list)
	