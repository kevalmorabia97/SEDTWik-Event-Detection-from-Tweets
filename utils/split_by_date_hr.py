import json

def split_by_hr(orig_file):
    """
    given a json file containing TWEETS FOR ONLY 1 DAY, split the files into different files based on the hour when it was written
    """
    hr_files = {}

    f = open(orig_file,'r')
    while True:
        line = f.readline().replace('\n','')
        if line == '': break
        tweet = json.loads(line)
        if not 'created_at' in tweet: continue # deleted tweet
        hr = tweet['created_at'].split(' ')[3].split(':')[0]
        if not hr in hr_files:
            print(hr)
            hr_files[hr] = open(hr + '_hour.json', 'a+')
        hr_files[hr].write(json.dumps(tweet)+'\n')
    f.close()    
        
    for hr in hr_files:
        hr_files[hr].close()
    print('DONE...')
    
def split_by_date(orig_file):
    """
    given a json file containing TWEETS FOR ONLY 1 MONTH, split the files into different files
    based on the month and date when it was written
    """
    date_files = {}

    f = open(orig_file,'r')
    while True:
        line = f.readline().replace('\n','')
        if line == '': break
        tweet = json.loads(line)
        if not 'created_at' in tweet: continue # deleted tweet
        date = tweet['created_at'].split(' ')[2]
        if not date in date_files:
            print(date)
            date_files[date] = open(date + '_date.json', 'a+')
        date_files[date].write(json.dumps(tweet)+'\n')
    f.close()    
        
    for date in date_files:
       date_files[date].close()
    print('DONE...')    
    

if __name__ == '__main__':
    #split_by_hr('2012-Oct-14.json')
    split_by_date('2012-Oct.json')