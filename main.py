import os

from EventSegmentClusterer import get_events, get_seg_similarity
from TimeWindow import TimeWindow
from TwitterEventDetector import TwitterEventDetector


# Parameters
original_tweet_dir = 'data/original_tweets/' # end with '/'
clean_tweet_dir = 'data/cleaned_tweets/without_retweets/' # end with '/'
subwindow_dir = 'data/cleaned_tweets/without_retweets/2012-10-12/' # each file is a subwindow in this folder
event_output_dir = 'results/2012-10-12/'
wiki_titles_file = 'data/enwiki-titles-unstemmed.txt'
seg_prob_file = 'data/seg_prob_2012_Oct_11-22.json'
wiki_Qs_file = 'data/WikiQsEng_non_zero_processed.json'

remove_retweets = True
max_segment_length = 4
hashtag_wt = 3
entities_only = False # False --> use #tag and @name only for event detection
default_seg_prob = 0.0000001 # for unknown segments
use_retweet_count = True
use_followers_count = True
n_neighbors = 4
threshold = 4 # for news_worthiness

ted = TwitterEventDetector(wiki_titles_file, seg_prob_file, wiki_Qs_file, remove_retweets, max_segment_length,
                           hashtag_wt, use_retweet_count, use_followers_count, default_seg_prob, entities_only)

# Tweet Cleaning
#ted.clean_tweets_in_directory(original_tweet_dir, clean_tweet_dir)

# Segment tweets and create TimeWindow
print('\nReading SubWindows')
subwindow_files = [f.name for f in os.scandir(subwindow_dir) if f.is_file()]

subwindows = []
for subwindow_name in subwindow_files[:6]: # read timewindow consisting 6 subwindows of 1 hour each
    print('SubWindow:',subwindow_name)
    sw = ted.read_subwindow(subwindow_dir + subwindow_name)
    subwindows.append(sw)
print('Done\n')    

tw = TimeWindow(subwindows)
print(tw)

#next_subwindow = ted.read_subwindow(subwindow_dir + subwindow_files[7])
#tw.advance_window(next_subwindow)
#print(tw)

# Bursty Segment Extraction
print()
bursty_segment_weights, segment_newsworthiness = ted.bse.get_bursty_segments(tw)
seg_sim = get_seg_similarity(bursty_segment_weights, tw)

# Clustering Bursty Segments
events = get_events(bursty_segment_weights, segment_newsworthiness, seg_sim, n_neighbors)

# dump event clusters along with tweets[cleaned ones :-( ] associated with the segments in the cluster 
print('\nEvents will be saved in', event_output_dir)
if not os.path.exists(event_output_dir):
    os.makedirs(event_output_dir)
event_no = 0
for e, event_worthiness in events:
    event_no += 1
    print('\nEVENT:', event_no, 'News Worthiness:', event_worthiness) 
    f = open(event_output_dir + str(event_no) + '.txt', 'w')
    f.write(str(e)+' '+str(event_worthiness)+'\n\n')
    for seg_name in e:
        print(seg_name) 
        f.write('SEGMENT:' + seg_name+'\n')
        for text in set(tw.get_tweets_containing_segment(seg_name)):
            f.write(text+'\n')
        f.write('-----------------------------------------------------------\n')
    f.close()

