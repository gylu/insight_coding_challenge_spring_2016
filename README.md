# Insight_coding_challenge

## The solution file to this coding challenge is src/average_degree.py 
#### Python 3 is used, therefore the environment needs to have it installed

### Overview of what src/average_degree.py does:
1.     Get tweets:
  1.     If it's a rate limiting message, ignore it
2.     Check timestamp:
  2.     If timestamp is older than 60s, delete tweet, jump to call calc_average_degree() to end
  2.     If timestamp is newer than newest, update newest_timestamp value
3.      Delete edges that are older than 60 seconds
4.     Find hashtags:
  4.     If tweet has 2 or most hashtags, check and remove all duplicates
  4.    If only 0 or 1 hashtag remains, discard tweet, jump to call calc_average_degree()
5.   	Create edge entries: (If tweet has 2 or more valid hashtags, create edge entries)
  5.     Use the combination package that was imported. Eg: list(combinations(['hashtag1','hashtag2','hashtag3'],2)). This outputs a list of tuples.
  5.    Sort each edge entry alphabetically so that we don't have the check the reverse. Do this by converting each tuple into a list and sorting
6.      Insert each new edge entry into edge_list:
  6.     Check that the edge doesn't already exist, if it does, update timestamp of that edge (no need to check for reverse order, because each edge entry is already sorted)
7.      call calc_average_degree()
  7.     concatenate the 2 columns of nodes in the edge_list, and sum
  7.    remove duplicates to get the number of nodes


### src/average_degree.py already imports all the pacakges it needs. 

The following packages are used/imported:

* import time - needed to deal with timestamps
* import sys - for reading the arugments of the run.sh command
* import json - for processing json
* import os - for checking if output.txt already exists, and deleting it if it does
* from itertools import combinations - used to run combinations (order doesn't matter), Taken from: https://rosettacode.org/wiki/Combinations#Python


#### Note that this repo started off as a clone of https://github.com/InsightDataScience/coding-challenge

#### Running and Testing:
I have been running the run.sh scripts with bash. E.g "bash ./run.sh" from the root directory.

For testing, I have been running "bash ./run_tests.sh" from within the insight_testsuite directory