import tweepy
import re
import json
import sys
import time
import HTMLParser
import redis
import threading

# Authentication details
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

class TagCloud():
	
	def __init__(self):
		# Load stop words
		self.stopWords = set()
		self.loadStopWords(self.stopWords)

		# Initialising other variables
		self.maxWords = 10 # default
		self.totalWords = 0

		# Setting redis
		self.words = redis.Redis(host='redis', port='6379')
		self.words.flushall()
	
	def addWordsToRedis(self, message):
		""" This adds a word / increments its value
		 in the redis dictionary
		"""
		for word in re.findall("[a-zA-Z0-9'@#_]+", message):
			if word not in self.stopWords:
				self.totalWords += 1
				self.words.zincrby("tagcloud", word)

	def parse(self, message):
		""" Deletes links
		"""
		message = re.sub('https?:\/\/[a-zA-Z0-9.]+\/[a-zA-Z0-9]*', '', message)
		self.addWordsToRedis(message.lower())

	def setMaxWords(self, maxWords):
		""" Sets the count of the top words to be shown
		"""
		self.maxWords = maxWords
		
	def getResults(self):
		""" Gets results from redis
		"""
		counter = 0
		arr = []

		results = self.words.zrevrangebyscore('tagcloud', 'inf', 
						0, start = 0, 
						num = self.maxWords, withscores=True)		

		for result in results:
			counter += int(result[1])
			arr.append({'word' : result[0], 'count' : int(result[1])})
		
		arr.append({'word' : 'other', 'count' : self.totalWords - counter})

		return arr
	

	def printResults(self):
		""" Prints top words
		"""
		results = self.getResults()
		json.dumps(results)
		print results

	def loadStopWords(self, stopWords):
		""" Loads stop words
		"""
		loadedWords = [line.strip() for line in open('stopwords.txt')]
		self.stopWords |= set(loadedWords)

# This is the listener, responsible for receiving data
class StdOutListener(tweepy.StreamListener):
	""" This listener handles tweets by passing them to the parser
	"""
	
	def __init__(self, tagCloud, event):
		self.tagCloud = tagCloud
		self.event = event

	def on_connect(self):
		""" This event tells the main thread when the streaming
		starts, so the countdown should start too
		"""
		self.event.set()
	
	def on_data(self, data):
		""" Process messages from Twitter
		"""
		decoded = json.loads(data)
		message = decoded['text'].encode('ascii', 'ignore')
		self.tagCloud.parse(HTMLParser.HTMLParser().unescape(message))
		return True

	def on_error(self, status):
		print(status)


if __name__ == '__main__':
		
	if len(sys.argv) == 3:
		# Event for starting the count
		event = threading.Event()

		# Initialising the Twitter listener
		tagCloud = TagCloud()
		listener = StdOutListener(tagCloud, event)

		# Authenticate
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		language = 'en'

		# Parse input data
		processTime = int(sys.argv[1])
		maxWords = int(sys.argv[2])
		tagCloud.setMaxWords(maxWords)

		print "Showing first " + str(maxWords) + " trending words for " + str(processTime) + " seconds:"
		
		# Start sample streaming
		stream = tweepy.Stream(auth, listener)
		stream.sample(async=True, languages=[language])

		# Wait for the stream to connect to Twitter
		event.wait()

		# The time when the listener thread must stop
		endTime = time.time() + processTime;

		# Streaming for given seconds
		while True:
			if time.time() > endTime:
				stream.disconnect()
				tagCloud.printResults()
				print "Done"
				break
	else:
		print "Usage: python2.7 SECONDS MAXWORDS"
		exit(0)
