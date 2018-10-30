class Segment:
    def __init__(self,segment):
        """
        segment           - string of words ex. 'steve jobs'
        tweets            - list of tweets( text:str ) containing this segment in current time window
        freq              - tweet-freq i.e. number of tweets containing this segment
        user_count        - no. of unique users that used this segment in current time window
        retweet_count     - sum of retweet counts of all tweets containing this segment
        followers_count   - sum of followers count of all users using this segment
        newsworthiness    - measure of importance of segment calculated by Twevent's Q(s) values
        """
        self.segment = segment
        self.tweets = []
        
        self.freq = 0
        self.user_set = set()
        self.retweet_count = 0
        self.followers_count = 0
        self.newsworthiness = 0
        
    def add_tweet(self, user_id, text, retweet_count, followers_count):    
        self.tweets.append(text)
        self.user_set.add(user_id)
        self.freq += 1
        self.retweet_count += retweet_count
        self.followers_count += followers_count
        
    def get_user_count(self):
        return len(self.user_set)
        
    def __str__(self):
        return 'Segment:'+self.segment+', freq:'+str(self.freq)+', user_count:'+str(self.get_user_count())

