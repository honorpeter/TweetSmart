import tweepy
import csv
import pandas as pd
import heapq 


class FreqStack(object):

    def __init__(self):
        self.freq = collections.Counter()
        self.group = collections.defaultdict(list)
        self.maxfreq = 0

    def push(self, x):
        f = self.freq[x] + 1
        self.freq[x] = f
        if f > self.maxfreq:
            self.maxfreq = f
        self.group[f].append(x)

    def pop(self):
        x = self.group[self.maxfreq].pop()
        self.freq[x] -= 1
        if not self.group[self.maxfreq]:
            self.maxfreq -= 1

        return x

# Twitter API credentials
consumer_key = 'IFPYrIpyKNqt8qe7GbQvw8NzQ'
consumer_secret = 'mo2eR5eoGLu595DaSKszFanUWcvYpTHKRIaRyvGnYHA4jUXOKi'
access_key = '779885459929337856-y0LNiqvm4EsFWDguaLW712p8e9c5MdH'
access_secret = 'tvxnYaWGgTaL1cwDF0QAGBKkeBvqYBSEgzbM9GwsUqkIX'

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

elon = []
d = {}
d['name'] = {}
d['tweet'] = {}


def get_all_tweets(screen_name):
	
	alltweets = []	
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	alltweets.extend(new_tweets)
	oldest = alltweets[-1].id - 1
	
	while len(new_tweets) > 0:
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1].id - 1
		#print("...%s tweets downloaded so far" % (len(alltweets)))
		outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]

		print(outtweets)
	

def getFavs(screen_name):

	likes = api.favorites(screen_name = screen_name)
	
	for like in likes:
    # Process a single status
	    
	    print("Username : ",like.user.screen_name)
	    print("Post : ",like.text)

	   #id,text,screen_name

def moreLikes(screen_name):
	max = 0
	name = ""
	for page in tweepy.Cursor(api.favorites,id=screen_name,wait_on_rate_limit=True, count=200).pages(200):
		for status in page:
			if status.user.screen_name in d['name']:
				d['name'][status.user.screen_name]+=1

				#if d['name'][status.user.screen_name] > max:
				#	name = status.user.screen_name
				#	max = d['name'][status.user.screen_name]
			#d['tweet'].append(status.text)
			else:
				d['name'][status.user.screen_name]=1

	#df = pd.DataFrame(d,columns = ['name','tweet'])
	#df_count = pd.DataFrame.from_dict(d['name'])
	#df.to_csv('mattGlanz.csv')
	sorted_by_value = sorted(d['name'].items(), key=lambda kv: kv[1])
	sorted_by_value.reverse()
	print(sorted_by_value)


if __name__ == '__main__':
	#get_all_tweets("nawalsanchit")
	moreLikes("MattGlantz")

