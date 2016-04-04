# insight_coding_challenge
The solution file to this coding challenge is src/average_degree.py. That file already imports all the pacakges it needs. The following packages are used/imported:

import sys - for reading the arugments of the run.sh command
import json - for processing json
import os - for checking if output.txt already exists, and deleting it if it does
from itertools import combinations - used to run combinations (order doesn't matter), Taken from: https://rosettacode.org/wiki/Combinations#Python


Overview of what the code does:
#edge_list will be of the form: timestamp, node1, node2
#1.     Get tweets:
#1a     If it's a rate limiting message, ignore it

#2.     Check timestamp and process accordingly:
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

