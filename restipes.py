import tweepy
import re
import requests
import config
from textblob import TextBlob


# Load keys from personal config
consumer_key = config.consumer_key;
consumer_secret = config.consumer_secret;

access_token = config.access_token;
access_token_secret = config.access_token_secret;

# Authorize access
auth = tweepy.OAuthHandler(consumer_key, consumer_secret);
auth.set_access_token(access_token, access_token_secret);

api = tweepy.API(auth)

# Search tweets containing string
public_tweets = api.search('recipe')

''' Use regex to find desired word in string and return search function '''
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

''' Check all returned tweets '''
for tweet in public_tweets:
	
	# Assume bad tweet
	goodTweet = False 
	# Convert tweet for analysis
	analysis = TextBlob(tweet.text) 
	link = ''
	# Assume no URL
	hasLink = False
	
	# Check for https
	hasLink = (findWholeWord('https')(tweet.text))

	# Regex filter non alphas
	regex = re.compile('[^a-zA-Z]')
	# Search nouns and delete non alphas
	for noun in analysis.noun_phrases:
		# Apply regex filter to noun
		noun = regex.sub('', noun)

	#Check for link
	if(hasLink):
		# Get link from tweet
		linkIndex = tweet.text.find('https')
		# Start index at URL index
		i = linkIndex
		# Assert URL begins correctly
		if(tweet.text[linkIndex + 5 : linkIndex + 8] == '://'):
			# Check no spaces exist in rest of tweet URL
			while (tweet.text[i] != ' ' and i < len(tweet.text))-1:
				i += 1
			# Save link
			link = tweet.text[linkIndex : linkIndex + i]
			# Check for commonly found error
			if(tweet.text[linkIndex+8] != '.'):
				goodTweet = True
	
	# IF tweet has valid URL and is not a question about a recipe		
	if(goodTweet and tweet.text.find('?') == -1):
		# If multiple links take first
		strs = link.split(" ",2)
		# Check tweet has positive sentiment above desired threshold
		if(analysis.sentiment >= 0.8):
			print("Tweet: " + tweet.text + '\n')
			print('Link: ' + strs[0])
			break

	# Provide spacing between tweets
	print('\n')

