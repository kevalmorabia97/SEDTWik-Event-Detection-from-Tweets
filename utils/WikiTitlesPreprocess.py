import re
import string 

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Latest Wiki titles file can be downloaded from https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-all-titles-in-ns0.gz
def preprocess_wiki_titles_file(wiki_file, output_file, remove_stopwords=True):
    """
    Preprocess Wiki Titles file to make is usable in the event detection model
    """
    print('Preprocessing Wiki Titles File.\nThis might take about an hour, so why dont you watch a TV Show meanwhile.\n')
        
    wiki_titles = set()
    
    if remove_stopwords: stop_words = set(stopwords.words('english'))
    else: stop_words = set()
    
    punc_table = str.maketrans("", "", string.punctuation) # to remove punctuation from each word in tokenize
    
    line_no = 0
    f = open(wiki_file, 'r', encoding="utf8")
    for line in f:
        line_no += 1
        if(line_no % 1000000 == 0): print(line_no)
        line = line.replace('\n','').replace('\"','').replace('-',' ').replace('_',' ')
        line = re.sub(r'\([^)]*\)','' , line) # remove text inside parenthesis
        line = re.sub(r'[0-9]*','' , line) # remove numbers
        line = ''.join([w if ord(w) < 128 else ' ' for w in line]) # remoce non ascii chars
        tokens = [w.translate(punc_table).lower() for w in word_tokenize(line)] # remove punctuations, tokenize, convert to lowercase
        
        tokens = [w for w in tokens if w not in stop_words and len(w)>1] # stem each word
        
        if not len(tokens) > 1: continue # keeps titles with more than 1 word 
        line = ' '.join(tokens)
        wiki_titles.add(line) # if present then not added in set
    f.close()
      
    f = open(output_file, 'w')    
    print('actual lines:',line_no)
    print('after preprocessing:',len(wiki_titles))
    
    for i in wiki_titles: f.write(i+'\n')
    f.close()
    
    print('DONE PREPROCESSING WIKI TITLES FILE!!!\n')
    
if __name__ == '__main__':
    wiki_file='enwiki-latest-all-titles-in-ns0'
    
    output_file='enwiki-titles-unstemmed.txt'
    preprocess_wiki_titles_file(wiki_file, output_file)