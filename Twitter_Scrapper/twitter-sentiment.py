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
import numpy as np
import pandas as pd


# # # TWITTER CLIENT # # #
class TwitterClient():
	
	def __init__(self, twitter_user=None):
		self.auth = TwitterAuthenticator().authenticate_twitter_app()
		self.twitter_client = API(self.auth)
		self.twitter_user = twitter_user

	def get_twitter_client_api(self):
		return self.twitter_client

	def get_user_timeline_tweets(self, num_tweets):
		tweets = []
		# Get tweets from that user timeleinedd
		for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
			tweets.append(tweet)
		return tweets

	def get_friend_list(self, num_friends):
		friend_list = []
		for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
			friend_list.append(friend)
		return friend_list

	def home_timeline_tweets(self, num_tweets):
		home_timeline_tweets = []
		for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
			home_timeline_tweets.append(tweet)
		return home_timeline_tweets
  
# # # TWITTER AUTHENTICATOR # # #
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
		if(status == 420):
			# Returning False on_data menthd in case rate limit occurs.
			return False
		print(status)


class TweetAnalyzer():
	"""
	Functionality for analyzing and categorizing content from tweets
	"""
	def tweets_to_dataframe(self, tweets):
		df = pd.DataFrame(data= [tweet.text for tweet in tweets ], columns=["Tweets"])
		
		df['id'] = np.array([tweet.id for tweet in tweets])
		df['source'] = np.array([tweet.source_url for tweet in tweets])
		df['retweet'] = np.array([tweet.retweet_count for tweet in tweets])
		df['language'] = np.array([tweet.lang for tweet in tweets])
		# df['possibly_sensitive'] = np.array([tweet.possibly_sensitive for tweet in tweets])

		return df

if __name__ == "__main__":
	
	# hashtag_list = ["Sushant Singh Rajput", "SSR", "MSD", "Mahendra Singh Dhoni"]
	# fetched_tweets_filename = "tweets.json"

	# twitter_client = TwitterClient('pycon')
	# print(twitter_client.get_user_timeline_tweets(1))
	# twitter_streamer = TwitterStreamer()
	# twitter_streamer.stream_tweets(fetched_tweets_filename, hashtag_list)
	api = TwitterClient().get_twitter_client_api()
	tweets = api.user_timeline(screen_name='elonmusk', count=21)
 
	# print(dir(tweets[0])) # Gives us the types of information that we can extract from each tweet
 
	df = TweetAnalyzer().tweets_to_dataframe(tweets)
	print(df.head())
	