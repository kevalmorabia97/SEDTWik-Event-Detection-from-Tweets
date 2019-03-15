from sklearn.feature_extraction.text import TfidfVectorizer

from Segment import Segment

        
def tf_idf_sim(text1, text2):
    try:
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0,1]
    except:
        return 0


class SubWindow:
    time_frame_counter = 0 # static var
    
    def __init__(self,segments, tweet_count):
        """
            segments is dict of Segment class objects indexed by segment name ex. 'selena gomez'
            tweet_count is number of tweets in this subwindow from which the segments are extracted
        """
        SubWindow.time_frame_counter += 1
        
        self.time_frame = SubWindow.time_frame_counter # unique time frame to each sub window starting from 1
        self.segments = segments
        self.tweet_count = tweet_count
    
    def __str__(self):
        result = 'SubWindow #'+str(self.time_frame)+', No. of Tweets: '+str(self.tweet_count)
        return result
         
    def get_tweets_containing_segment(self,segment):
        return self.segments[segment].tweets
    
    def get_freq_of_segment(self, segment):
        return self.segments[segment].freq

    def get_user_count_for_segment(self, segment):
        return self.segments[segment].get_user_count()
    
########## END OF CLASS SubWindow ##########    


class TimeWindow:

    def __init__(self, initial_subwindows):
        """
        initial_subwindows = list of SubWindow objects
        """
        self.no_of_subwindows = len(initial_subwindows)
        self.subwindows = initial_subwindows
        self.start_frame = 1
        self.end_frame = self.no_of_subwindows # time frame starting from 1
    
    def __str__(self):
        result = ''
        result += '----- TimeWindow['+str(self.start_frame)+'-'+str(self.end_frame)+'] -----\n'
        result += 'No. of Tweets: '+str(self.get_tweet_count())
        for sw in self.subwindows: result += '\n'+sw.__str__()
        return result
        
    def get_tweet_count(self):
        return sum([sw.tweet_count for sw in self.subwindows])   
    
    def get_segment_names(self):
        segment_names = set()
        for sw in self.subwindows:
            for seg in sw.segments:
                segment_names.add(seg) 
        return segment_names
    
    def get_tweets_containing_segment(self, seg_name):
        tweets = []
        for sw in self.subwindows:
            segment = sw.segments.get(seg_name,None)
            if not segment == None:
                tweets += segment.tweets
        return tweets
        
    def advance_window(self, next_subwindow):
        print('Advancing Time Window')
        self.subwindows = self.subwindows[1:]
        self.subwindows.append(next_subwindow)
        self.start_frame += 1
        self.end_frame += 1
        
    def get_segment_similarity(self, s1_name, s2_name):
        """
        return similarity of 2 Segment names using TF-IDF similarity of their tweets
        """
        
        s1_freq = 0 # total freq of segment 1 in time window
        s2_freq = 0
        
        similarity = 0
        for sw in self.subwindows:

            s1 = sw.segments.get(s1_name, None)
            s2 = sw.segments.get(s2_name, None)
            
            if not s1 == None: s1_freq += s1.freq
            if not s2 == None: s2_freq += s2.freq
            
            if s1 == None or s2 == None: continue
            
            similarity += s1.freq * s2.freq * tf_idf_sim(' '.join(s1.tweets), ' '.join(s2.tweets))
            
        similarity = similarity/(s1_freq * s2_freq)
        return similarity

########## END OF CLASS TimeWindow ##########