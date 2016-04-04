import sys
import os
import json #use for json parser
from itertools import combinations #used to run combinations (order doesn't matter)
import time #needed to deal with timestamps

#Note: From the way run.sh is called:
#print(sys.argv[0]) #will be the name of this script: average_degree.py
#print(sys.argv[1]) #will be ./tweet_input/tweets.txt 
#print(sys.argv[2]) #Will be ./tweet_output/output.txt

#todo replace:
# sys_argv0 replace for sys.argv[0]
# sys_argv1
# sys_argv2
sys_argv1 = './tweet_input/tweets.txt'
sys_argv2 = './tweet_output/output.txt'
#todo:
#remove tweet_input/tweets.txt from the gitignore

#edge_list will be of the form: timestamp, node1, node2
#1.     Get tweets:
#1a     If it's a rate limiting message, ignore it

#2.     Check timestamp and:
#2b     If timestamp is older than 60s, delete tweet, call calc_average_degree()
#2c     If timestamp is not older than 60s, process the tweet

#3.     Processing the tweet:
#3a     If timestamp is newer than newest, update newest_timestamp value
#3b     Clean the edge list: Delete edges that are older than 60 seconds
#3c     If tweet has 2 or most hashtags, check and remove all duplicates
#3d     If only 0 or 1 hashtag remains, discard

#4      Create edge entries for each tweet that still has 2 or more distinct hashtags:
#4a     Use the combination packcage that was imported. Eg: list(combinations(['hashtag1','hashtag2','hashtag3'],2)). This outputs a list of tuples.
#4b     Sort each edge entry alphabetically so that we don't have the check the reverse. Do this by converting each tuple into a list and sorting

#5      Insert each new edge entry into edge_list:
#5a     Check that the edge (and the reverse) doesn't already exist, if it does, remove the older edge


#7      call calc_average_degree()
#7a     concatenate the 2 columns of nodes in the edge_list, and sum
#7b     remove duplicates to get the number of nodes




#1. Get tweets
#clear out old ./tweet_output/tweets.txt file
if os.path.exists(sys_argv2):
    os.remove(sys_argv2) #note that the location is based on where run.sh was called

#1a. Ignore the rate limiting messages
#future optimization: this may be able to be optimized to process one-at-a-time as each json object line in the text file is read
tweets = []
for line in open(sys_argv1, 'r'):
    line_json_parsed = json.loads(line)
    if 'created_at' in line_json_parsed: #ignore the limit stuff
        tweets.append(line_json_parsed)

# #Example usage of the tweets array that examples the 248th tweet in the file
# tweets[248] # fetches a tweet
# tweets[248]['created_at'] # fetches timestamp of tweet
# tweets[248]['entities']['hashtags'] # fetches all hashtags of a tweet
# tweets[248]['entities']['hashtags'][1] # fetches individual hashtag of a tweet
# tweets[248]['entities']['hashtags'][1]['text'] # fetch individual hashtag text of a tweet
# len(tweets[248]['entities']['hashtags']) #tells you how many hashtags the tweet had

newest_timestamp=0.00;
#check timestamp

for tweet in tweets:
    tweetWithinTimeRange = checkTimeStamp_withinRange(tweet['created_at']); #note that this created_at field is always utc time
    if (!tweetWithinTimeRange):
        calc_average_degree();
    else:


def checkTimeStamp_withinRange( newTimeStampToBeChecked ):
    #newTimeStampToBeChecked is something in the format of "Wed Aug 29 17:12:58 +0000 2012"
    timestampToBeChecked_epoch_utc = time.mktime(time.strptime(created_at,"%a %b %d %H:%M:%S +0000 %Y")) #followed this http://stackoverflow.com/questions/18604755/twitter-created-at-convert-epoch-time-in-python
    if timestampToBeChecked_epoch_utc < newest_timestamp -60:
        return false
    else if timestampToBeChecked_epoch_utc > newest_timestamp:
        newest_timestamp=timestampToBeChecked_epoch_utc;
    return true
 
def calc_average_degree():
    return true