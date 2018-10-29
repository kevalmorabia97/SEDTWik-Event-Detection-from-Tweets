import os
import time

from TwitterEventDetector import *

print('Started at:',time.ctime())

# ## Parameters
original_tweet_dir = '../data/original_tweets/' # end with '/'
clean_tweet_dir = '../data/cleaned_tweets/without_retweets/' # end with '/'
subwindow_dir = '../data/cleaned_tweets/without_retweets/2012-10-17/' # each file is a subwindow in this folder
event_output_dir = '../Results/'
wiki_titles_file='../data/enwiki-titles-unstemmed.txt'
seg_prob_file='../data/seg_prob_2012_Oct_11-22.json'
common_words_file = '../data/common_words.txt'

remove_stopwords=True
remove_retweets=True
max_segment_length=4
hashtag_wt=3
entities_only = False
default_seg_prob=0.0000001
use_retweet_count=True
use_followers_count=True
n_neighbors=4
min_cluster_segments=5

# ## Initialization
print('\nParameters:')
print('Tweets dir', subwindow_dir.split('/')[-2])
print('remove_stopwords', remove_stopwords)
print('remove_retweets', remove_retweets)
print('max_segment_length', max_segment_length)
print('hashtag_wt', hashtag_wt)
print('entities_only', entities_only)
print('use_retweet_count', use_retweet_count)
print('use_followers_count', use_followers_count)
print('default_seg_prob', default_seg_prob)
print('clustering n_neighbors', n_neighbors)
print('min_cluster_segments', min_cluster_segments)
print()

common_words = set()

f = open(common_words_file, 'r')
while True:
    line = f.readline()
    if line == '': break
    common_words.add(line.replace('\n',''))
f.close()

ted = TwitterEventDetector(wiki_titles_file, seg_prob_file, remove_stopwords,remove_retweets, max_segment_length,
                           hashtag_wt, use_retweet_count, use_followers_count, default_seg_prob, common_words, entities_only)

# ## Tweet Cleaning
#ted.clean_tweets_in_directory(original_tweet_dir, clean_tweet_dir)

# ## Segment tweets and create TimeWindow
print('\nReading SubWindows')

subwindow_files = [f.name for f in os.scandir(subwindow_dir) if f.is_file()]

subwindows = []
for subwindow_name in subwindow_files[:3]: # read given subwindows
    print('SubWindow:',subwindow_name)
    sw = ted.read_subwindow(subwindow_dir + subwindow_name)
    subwindows.append(sw)
print('Done\n')    

tw = TimeWindow(subwindows)
print(tw)

#next_subwindow = ted.read_subwindow(subwindow_dir + subwindow_files[4])
#tw.advance_window(next_subwindow)
#print(tw)

# ## Bursty Segment Extraction
print()
bursty_segment_weights = ted.bse.get_bursty_segments(tw) # dict from seg_name to bursty_wt
seg_sim = get_seg_similarity(bursty_segment_weights, tw)

# ## Clustering Bursty Segments
print()
for n_neighbors,min_cluster_segments in [(2,5), (3,7), (4,10)]:
    print('No. of Neighbors', n_neighbors)
    print('Min Cluster Segments', min_cluster_segments)
    events = get_events(bursty_segment_weights, seg_sim, n_neighbors, min_cluster_segments)
    event_no = 0
    for e,avg_score in events:
        event_no += 1
        print(event_no, e)
    print('-----------------------------------------------------------------------------------------------')
print('Ended at:',time.ctime())

