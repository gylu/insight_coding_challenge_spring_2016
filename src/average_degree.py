# Things to be done:
# 1. Build graph: e.g. list of edges with time stamp: "hashtags = [Spark , Apache],        created_at: Thu Mar 24 17:51:10 +0000 2016"
## 1a. maintain list of valid nodes
# 2. count degree for each edge for each node
# 3. Find average

import sys
import os
import json #use for json parser

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

#1. clear out old ./tweet_output/tweets.txt file
if os.path.exists(sys_argv2):
    os.remove(sys_argv2) #note that the location is based on where run.sh was called

#Parse the input file
#tweets_file = open(sys.argv[1])
#tweets_json_format=json.load(tweets_file)

#future optimization: this may be able to be optimized to process one-at-a-time as each json object line in the text file is read
tweets = []
for line in open(sys_argv1, 'r'):
    line_json_parsed = json.loads(line)
    if 'created_at' in line_json_parsed: #ignore the limit stuff
        tweets.append(line_json_parsed)

#example usage of the tweets array that examples the 248th tweet in the file
tweets[248] # fetches a tweet
tweets[248]['created_at'] # fetches timestamp of tweet
tweets[248]['entities']['hashtags'] # fetches all hashtags of a tweet
tweets[248]['entities']['hashtags'][1] # fetches individual hashtag of a tweet
tweets[248]['entities']['hashtags'][1]['text'] # fetch individual hashtag text of a tweet
len(tweets[248]['entities']['hashtags']) #tells you how many hashtags the tweet had


#if number of hashtags is 0, just add the tweet
#if number of hashtags is 1, remove the tag and add the tweet to the list (remove tag because list will be counted tags)

#edge_list will be of the form: timestamp, number of hashtags, node1, node2

#1.     Get tweets
#1a     If it's a rate limiting message, ignore it

#2.     Check timestamp and process accordingly
#2b     If timestamp is older than 60s, delete tweet, call calc_average_degree()
#2c     If timestamp is not older than 60s, process the tweet

#3.     Processing the tweet:
#3a     If timestamp is newer than newest, update newest_timestamp value
#3b     Clean the edge list: Delete edges that are older than 60 seconds
#3c     If tweet has 2 or most hashtags, check and remove all duplicates
#3d     If only 0 or 1 hashtag remains, discard

#4     Otherwise, If tweet has 2 or more distinct hashtags, create edge entry from each hashtag

#5      Insert edge entry into edge_list
#5a     Check that the edge and the reverse of that edge entry both don't already exist, if it does, remove the older edge


#7      call calc_average_degree()
#7a     concatenate the 2 columns of nodes in the edge_list, and sum
#7b     remove duplicates to get the number of nodes





#get hashtags
#remove repeat hashtags
#graph[0]['timestamp'] = timestamp
#graph[1]

# get_tweet
# check_timestamp
#     if (older than 60 sec from newest?)
#         call throw out
#     else
#         newer than newest? 
#             update newest
#             run throw out oldest
#         older than oldest? update oldest
