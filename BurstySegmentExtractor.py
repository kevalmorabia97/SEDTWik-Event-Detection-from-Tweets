from collections import OrderedDict
import json
from math import exp, sqrt, log10


class BurstySegmentExtractor():
    """
    Extract top k segments based on burst weight of the segment in a given TimeWindow class object 
    for a segment, BurstyWeight = BurstProbability x log(user_freq) x log(retweet_count) x log(follower_count)
    """
    def __init__(self, seg_prob_file, use_retweet_count=True, use_followers_count=True, default_seg_prob=0.000001):
        """
        seg_prob_file: file containing expected probability of a segment to be used in a tweet
        use_retweet_count: whether to use retweet counts of tweet containing the segment to calculate bursty weight (default=True)
        use_followers_count: whether to use followers count of user using the segment to calculate bursty weight (deafult=True)
        seg_prob of a newly found segment is assumed to default_seg_prob (deafult - 0.000001)
        """
        print('Initializing BurstySegmentExtractor')
        
        with open(seg_prob_file,'r') as f:
            self.seg_prob = json.load(f)
        
        self.use_retweet_count = use_retweet_count
        self.use_followers_count = use_followers_count
        self.default_seg_prob = default_seg_prob
        
        print('BurstySegmentExtractor Ready')
    
    def get_bursty_segments(self, time_window):
        """
        return top k=sqrt(N) segments where N = no of tweets in time window in a dict with value equal to bursty weight
        Also return their news_worthiness values in a dict
        """
        
        print('Extracting Bursty Segments')
        
        segments = [] # list of (segment_names,bursty_weight)
        tweet_count = time_window.get_tweet_count()
        k = int(sqrt(tweet_count))
        
        for seg_name in time_window.get_segment_names():
            freq = 0
            user_set = set()
            retweet_count = 0 # sum of retweet counts of all tweets containing this segment
            followers_count = 0 # sum of followers counts of all users using this segment
            newsworthiness = 0
            for sw in time_window.subwindows:
                segment = sw.segments.get(seg_name,None)
                if not segment == None:
                    freq += segment.freq
                    user_set = user_set.union(segment.user_set)
                    retweet_count += segment.retweet_count
                    followers_count += segment.followers_count
                    newsworthiness = segment.newsworthiness
            
            user_count = len(user_set)
                
            prob = self.seg_prob.get(seg_name,self.default_seg_prob) # new segment

            seg_mean = tweet_count * prob
            seg_std_dev = sqrt(tweet_count * prob * (1 - prob))
            
            bursty_score = self.sigmoid(10 * (freq - seg_mean - seg_std_dev)/(seg_std_dev)) * log10(1+user_count)
            if self.use_retweet_count:
                bursty_score *= log10(1+retweet_count)
            if self.use_followers_count:
                bursty_score *= log10(1 + log10(1 + followers_count))

            segments.append((seg_name, bursty_score, newsworthiness))    
        
        print('Total Segments:',len(segments))
        print('Bursty Segments:',k)
        
        bursty_segment_weights = OrderedDict()
        segment_newsworthiness = {}
        for seg, b_score, newsworthiness in sorted(segments, key = lambda x : x[1], reverse=True)[:k]:
            bursty_segment_weights[seg] = b_score
            segment_newsworthiness[seg] = newsworthiness
            
        return bursty_segment_weights, segment_newsworthiness
    
    def sigmoid(self, x):
        try:
            return 1/(1+exp(-x))
        except:
            print('SIGMOID ERROR:', x)
            return 0
