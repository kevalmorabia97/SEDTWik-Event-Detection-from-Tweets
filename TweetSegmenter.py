import json
import math
import re


## IMPROVEMENT that can be done: What if in tweet = <w1,w2,w3>, <w1,w2> is in wiki and <w2,w3> is also there. Which segmentation to prefer?
class SEDTWikSegmenter:
    def __init__(self, wiki_titles_file, max_segment_length=4, hashtag_wt=3, entities_only=False):
        """
        Segment tweet based on Wikipedia Page Titles (processed by pyTweetCleaner.py)
        tweet_text should be processed by pyTweetCleaner.py before segmenting i.e. lowercase without hyperlinks, punctuations, non-ascii chars, stopwords, hashtags, @name
        max_segment_length = longest allowed no of words in a segment (default=4) 
        hashtag_wt(int) is the weight given to #tags as compared to other segments of the text (default = double weight)
        entities_only(True/False) if True then use only hashtags and @names
        NOTE: #tags are splitted and considered a segment
        NOTE: @username mentions are replaced by full name of user and considered a segment
        """
        print('Initializing SEDTWik Segmenter')
        
        wiki_titles = {} # 2 level dict, 1st level is 'a' to 'z' and 'other' to make search faster!!
        for i in range(97,123):
            wiki_titles[chr(i)] = set()
        wiki_titles['other']= set()

        f = open(wiki_titles_file, 'r')
        for title in f:
            title = title.replace('\n','')
            index = ord(title[0])
            if index in range(97,123): wiki_titles[chr(index)].add(title)
            else: wiki_titles['other'].add(title)    
                    
        self.wiki_titles = wiki_titles
        
        self.max_segment_length = max_segment_length
        self.hashtag_wt = hashtag_wt
        self.entities_only = entities_only
        
        print('SEDTWik Segmenter Ready\n')
     
    def compound_word_split(self, compound_word):
        """
        Split a given compound word containing alphabets into multiple words separated by space
        Ex: 'pyTWEETCleaner' --> 'py tweet cleaner'
        """
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', compound_word)
        return ' '.join([m.group(0) for m in matches]).lower()
     
    def is_title_present(self, title):
        """
        check if given title(string) is in wiki_titles
        """
        index = ord(title[0])
        if index in range(97,123): return title in self.wiki_titles[chr(index)]
        else: return title in self.wiki_titles['other']    
     
    def text_segmentation(self, tweet_text):
        """
        Perform the segmentation(list of segments(string)) of a tweet_text(string)
        """
        tokens = tweet_text.split()
        
        word_count = len(tokens)
        segmentation = []
        
        i = 0
        while i < word_count:
            j = min(i + self.max_segment_length, word_count) # check if tokens[i:j] is a title otherwise decrease j
            while True:
                seg = ' '.join(tokens[i:j])
                if self.is_title_present(seg):
                    segmentation.append(seg)
                    i = j
                    break
                elif j == i+1: # one word
                    #segmentation.append(tokens[i])
                    i += 1
                    break
                else:
                    j -= 1
        
        segmentation = [s for s in segmentation if len(s)>2]
        return segmentation
    
    def tweet_segmentation(self, json_tweet):
        """
        Perform the segmentation(list of segments(string)) of a json_tweet(dict)
        """
        if self.entities_only:
            segmentation = []
        else:
            segmentation = self.text_segmentation(json_tweet['text'])

        for um in json_tweet['entities']['user_mentions']: # list containing actual names of @name mentions in the tweet text
            um = re.sub('[^a-zA-Z ]+', '', um).strip().lower() # remove non-aplha chars
            um = re.sub(' +',' ',um) # replace multiple spaces by single
            if len(um) > 2:
                segmentation.append(um)
        
        for ht in json_tweet['entities']['hashtags']: # list containing hashtag texts of the tweet text
            ht = re.sub('[0-9]+','',ht) # remove digits
            ht = ' '.join([self.compound_word_split(i) for i in ht.split('_') if len(i)>0])
            if len(ht)>2:
                segmentation += [ht] * self.hashtag_wt
        
        return segmentation
    
if __name__ == '__main__':
    segmenter = SEDTWikSegmenter(wiki_titles_file='data/enwiki-titles-unstemmed.txt')

    while True:
         print('Enter Tweet to segment it ("x" to exit)...')
         tweet_text =  str(input())
         if tweet_text =='x': break
         print('Segmentation:', segmenter.text_segmentation(tweet_text),'\n')