from collections import OrderedDict
import json
import os
import sys

from BurstySegmentExtractor import *
from EventSegmentClusterer import *
from Segment import *
from TimeWindow import *
from TweetSegmenter import WikiTweetSegmenter
from utils.pyTweetCleaner import *


class TwitterEventDetector():
    
    def __init__(self, wiki_titles_file, seg_prob_file, remove_stopwords=True, remove_retweets=False, max_segment_length=4, hashtag_wt=2, use_retweet_count=True, use_followers_count=True, default_seg_prob=0.000001, common_words=set(), entities_only=False):
        self.segmenter = WikiTweetSegmenter(wiki_titles_file, max_segment_length, hashtag_wt, entities_only)

        self.remove_stopwords = remove_stopwords
        self.remove_retweets = remove_retweets
        self.common_words = common_words
        
        self.bse = BurstySegmentExtractor(seg_prob_file, use_retweet_count, use_followers_count, default_seg_prob)        
    
    def clean_tweets_in_directory(self, root_dir, target_dir):
        """
        clean tweets in root_dir using pyTweetCleaner and save cleaned files in target_dir
        """
        print('Cleaning all tweets in given directory')
        tc = TweetCleaner(self.remove_stopwords, self.remove_retweets)
        if not os.path.isdir(target_dir): os.mkdir(target_dir)
        for dir_path, sub_dir_list, file_list in os.walk(root_dir):
            dir_path = dir_path.replace('\\','/') # make windows-like path to unix-like path which can be used for both
            dir_name = dir_path.replace(root_dir,'') 
            print('Found directory: %s' % dir_name)
            target_file_path = target_dir+'/'+dir_name
            if not os.path.isdir(target_file_path): os.mkdir(target_file_path)
            for fname in file_list:
                print(fname)
                tc.clean_tweets(input_file=dir_path+'/'+fname, output_file=target_file_path+'/'+fname)
        print('Cleaned all tweets and saved to',target_dir)        
    
    def read_subwindow(self, file_path):
        """
        read a SubWindow from a file
        all tweets in given file belong to the subwindow
        """
        segments = {}
        tweet_count = 0
        f = open(file_path, 'r')
        for line in f:
            line = line.replace('\n','')
            if line == '': continue
            json_tweet = json.loads(line)
            tweet_count += 1
            user_id = json_tweet['user']['id']
            retweet_count = json_tweet['retweet_count']
            followers_count = json_tweet['user']['followers_count']
            segmentation = self.segmenter.tweet_segmentation(json_tweet)
            segmentation = [i for i in segmentation if not i in self.common_words]
            tweet_text = ' '.join(list(OrderedDict.fromkeys(segmentation))) # because of hashtag_wt, some segments might be multiple in tweet text after joining so remove them
            tweet_text = ''.join([c for c in tweet_text if ord(c)<256]) # dont know why but some non ascii chars like \u0441='c'still survived segmentation!!!
            for seg in segmentation:
                if not seg in segments: segments[seg] = Segment(seg)
                segments[seg].add_tweet(user_id, tweet_text, retweet_count, followers_count)
        f.close()
        
        sw = SubWindow(segments, tweet_count)
        return sw

if __name__ == '__main__':
    ted = TwitterEventDetector(remove_stopwords=True, remove_retweets=True, max_segment_length=4)