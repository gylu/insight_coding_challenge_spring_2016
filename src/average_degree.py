#!/usr/bin/env python3

# Overview of what this code does:
# 1.     Get tweets:
# 1a     If it's a rate limiting message, ignore it

# 2.     Check timestamp:
# 2a     If timestamp is older than 60s, delete tweet, jump to call calc_average_degree() to end
# 2b     If timestamp is newer than newest, update newest_timestamp value

# 3      Delete edges that are older than 60 seconds

# 4      Find hashtags:
# 4a     If tweet has 2 or most hashtags, check and remove all duplicates
# 4b     If only 0 or 1 hashtag remains, discard tweet, jump to call calc_average_degree()

# 5      Create edge entries: (If tweet has 2 or more valid hashtags, create edge entries)
# 5a     Use the combination package that was imported. Eg: list(combinations(['hashtag1','hashtag2','hashtag3'],2)). This outputs a list of tuples.
# 5b     Sort each edge entry alphabetically so that we don't have the check the reverse. Do this by converting each tuple into a list and sorting

# 6      Insert each new edge entry into edge_list:
# 6a     Check that the edge (and the reverse) doesn't already exist, if it does, remove the older edge

# 7      call calc_average_degree()
# 7a     concatenate the 2 columns of nodes in the edge_list, and sum
# 7b     remove duplicates to get the number of nodes

#Note that tweet_input/tweets.txt is listed in gitignore because it's so big



####### Implementation of the above outline #######

import sys
import os
import json #use for json parser
from itertools import combinations #used to run combinations (order doesn't matter)
import time #needed to deal with timestamps

#Note: From the way run.sh is called:
#print(sys.argv[0]) #will be the name of this script: average_degree.py
#print(sys.argv[1]) #will be ./tweet_input/tweets.txt 
#print(sys.argv[2]) #Will be ./tweet_output/output.txt

sys_argv0 = sys.argv[0]
sys_argv1 = sys.argv[1] #'./tweet_input/tweets.txt'
sys_argv2 = sys.argv[2] #'./tweet_output/output.txt'

NEWEST_TIMESTAMP=0.00; #global vairable
EDGE_LIST=[] #of the format: [[timestamp1,['hashtagX1','hashtagY1']], [timestamp2,['hashtagX2','hashtagY2']], ...etc]
OUTPUT_FILE=""
DEBUG=False;



def main():
    global NEWEST_TIMESTAMP
    global EDGE_LIST
    global OUTPUT_FILE
    global DEBUG
    #clear out old ./tweet_output/tweets.txt file
    if os.path.exists(sys_argv2):
        os.remove(sys_argv2) #note that the location is based on where run.sh was called
    OUTPUT_FILE = open(sys_argv2, 'a+')

    #1. Get tweets
    #future optimization: this may be able to be optimized to process one-at-a-time as each json object line in the text file is read
    tweets = []
    for line in open(sys_argv1, 'r'):
        line_json_parsed = json.loads(line)
        if 'created_at' in line_json_parsed: #1a. Ignore the rate limiting messages
            tweets.append(line_json_parsed)
            # #Example usage of the tweets array that examples the 248th tweet in the file
            # tweets[248] # fetches a tweet
            # tweets[248]['created_at'] # fetches timestamp of tweet, returns in the format of "Wed Aug 29 17:12:58 +0000 2012"
            # tweets[248]['entities']['hashtags'] # fetches all hashtags of a tweet
            # tweets[248]['entities']['hashtags'][1] # fetches individual hashtag of a tweet
            # tweets[248]['entities']['hashtags'][1]['text'] # fetch individual hashtag text of a tweet
            # len(tweets[248]['entities']['hashtags']) #tells you how many hashtags the tweet had

    for tweet in tweets:
        tweet_timestamp = time.mktime(time.strptime(tweet['created_at'],"%a %b %d %H:%M:%S +0000 %Y")) #followed this http://stackoverflow.com/questions/18604755/twitter-created-at-convert-epoch-time-in-python
        if DEBUG: print("\nNew tweetTimestamp: ",tweet_timestamp);
        if (check_and_update_timestamp(tweet_timestamp)):     #2. Check timestamp: #note that this created_at field is always utc time
            if DEBUG: print("updated NEWEST_TIMESTAMP: ",NEWEST_TIMESTAMP)
            if DEBUG: print("EDGE_LIST before clean: ", EDGE_LIST)
            EDGE_LIST = [entry for entry in EDGE_LIST if entry[0] > NEWEST_TIMESTAMP-60] # 3      Delete edges that are older than 60 seconds
            if DEBUG: print("EDGE_LIST after clean: ", EDGE_LIST)
            validHashtags=find_hashtags(tweet)         #4      Find hashtags:
            if(len(validHashtags)>1):
                new_list_of_edges=create_edge_entries(validHashtags);             #5      Create edge entries:
                update_edge_list(new_list_of_edges,tweet_timestamp);
                if DEBUG: print("EDGE_LIST after update: ", EDGE_LIST)
        calc_average_degree();             #6      Insert each new edge entry into edge_list:
    OUTPUT_FILE.close();


####### Functions are defined here #######

#2.     Check timestamp:
#2a     If timestamp is older than 60s, delete tweet, jump to call calc_average_degree()
#2b     If timestamp is newer than newest, update newest_timestamp value
def check_and_update_timestamp( timestampToBeChecked_epoch_utc ): 
    global NEWEST_TIMESTAMP
    if DEBUG: print("prev NEWEST_TIMESTAMP: ",NEWEST_TIMESTAMP)
    if (timestampToBeChecked_epoch_utc < NEWEST_TIMESTAMP-60):
        return False
    elif (timestampToBeChecked_epoch_utc > NEWEST_TIMESTAMP):
        NEWEST_TIMESTAMP=timestampToBeChecked_epoch_utc;
    return True #whether or not this was the newest timestamp or just a valid one, return true
 
#4      Find Hashtags:
#4a     If tweet has 2 or most hashtags, check and remove all duplicates
#4b     If only 0 or 1 hashtag remains, discard tweet
def find_hashtags(tweet):
    hashtags=[]
    if (len(tweet['entities']['hashtags'])>0):
        for tweet_entity_hashtag in tweet['entities']['hashtags']:
            hashtags.append(tweet_entity_hashtag['text']);
        hashtags=list(set(hashtags)) #remove duplicates. Note that this could still return just 1 hashtag
    return hashtags

#5a     Use the combination package that was imported. Eg: list(combinations(['hashtag1','hashtag2','hashtag3'],2)). This outputs a list of tuples.
#5b     Sort each edge entry alphabetically so that we don't have the check the reverse. Do this by converting each tuple into a list and sorting
def create_edge_entries(listOfHashtags):
    new_list_of_tuple_edges=list(combinations(listOfHashtags,2))
    new_list_of_edges = [sorted(element) for element in new_list_of_tuple_edges]
    return new_list_of_edges

#6      Insert each new edge entry into edge_list:
#6a     Check that the edge doesn't already exist, if it does, update timestamp of that edge (no need to check for reverse order, because each edge entry is already sorted)
def update_edge_list(new_list_of_edges,tweet_timestamp):
    global EDGE_LIST
    for new_edge_to_be_added in new_list_of_edges:
        edge_doesnt_exist_yet=True;
        for element in EDGE_LIST:
            if (element[1]==new_edge_to_be_added):
                edge_doesnt_exist_yet=False;
                if(element[0]<tweet_timestamp):
                    element[0]= tweet_timestamp;
                break;
        #looped through whole existing EDGE_LIST and didn't break out of 2nd for loop, meaning this is a new edge
        if edge_doesnt_exist_yet:
            EDGE_LIST.append([tweet_timestamp,new_edge_to_be_added])
    return True;

#7      call calc_average_degree()
#7a     concatenate the 2 columns of nodes in the edge_list, and sum
#7b     remove duplicates to get the number of nodes
def calc_average_degree():
    global EDGE_LIST
    global OUTPUT_FILE
    all_edges=getColumn(EDGE_LIST,1)
    sumDegrees=2*len(all_edges);
    list_of_all_nodes = set([item for sublist in all_edges for item in sublist]) #followed this: http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    num_nodes=len(list_of_all_nodes)
    average_degree_untruncated=0.00
    if (num_nodes==0):
        OUTPUT_FILE.write('0.00') 
    else:  
        average_degree_untruncated=sumDegrees/num_nodes;
        average_degree='%.2f'%(average_degree_untruncated);
        OUTPUT_FILE.write(average_degree)
    OUTPUT_FILE.write("\n")
    return True;

#helper function for getting columns
def getColumn(matrix, i):
    return [row[i] for row in matrix]



if __name__ == "__main__":
    main()