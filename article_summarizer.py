# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 19:53:13 2018

@author: AbdulHafeez Consult
"""

from bs4 import BeautifulSoup
import requests
#this returns title and text of an article
def get_only_text_washington_post_url(url):

    
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc)
#    print(soup.prettify())
    title=soup.title.text
    article = ' '.join([p.text for p in soup.findAll('p')])

    return title, article
#
#import nltk
#nltk.download()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
wordnet_lemmatizer = WordNetLemmatizer()
from nltk.stem.porter import PorterStemmer

stopWords = set(stopwords.words("english"))
#this processes text by removing stopwords, toknenizing,, stemming, lemmatizing
def cleanText(text): 
    words = word_tokenize(text)
    nS_word = [t for t in words if t not in stopwords.words('english')]
    lemma_article=[wordnet_lemmatizer.lemmatize(t,'v') for t in nS_word]
    ps=PorterStemmer()
    stem_article=[ps.stem(word) for word in lemma_article]
    alpha_article=[t for t in stem_article if t.isalpha()]
    return alpha_article

#this summarizes the pox=cessed text
def summarize(text,n):
    cleanTexts=cleanText(textOfUrl[1])
    freqTable=dict()
    for word in cleanTexts:
        if word in freqTable:
            freqTable[word]+=1
        else:
            freqTable[word]=1    
    maxFreq=max(freqTable.values())
#words with too much/less frequency are most likely unimportant words
#we normalize so al words value are between 0-1 and words not within 0.1-0.9 are removed
    min_cut=0.1
    max_cut=0.9
    for w in list(freqTable.keys()):
        freqTable[w]=freqTable[w]/maxFreq
    #for w in list(freqTable.keys()):
        if freqTable[w] >= max_cut or freqTable[w] <= min_cut:
            del freqTable[w]
    for w in freqTable.keys():
        freqTable[w]=freqTable[w]*maxFreq
    
    sentences =sent_tokenize(text)
    word_sent = [word_tokenize(s.lower()) for s in sentences]
    
    
    from collections import defaultdict
    sentenceValue=defaultdict(int)
    
#assign values or scores too sentences based on frequent words in the frequency table
    
    for i, sent in enumerate(word_sent):
        for w in sent:
            if w in freqTable:
                sentenceValue[i] += freqTable[w]
#this helps with the ranking of the sentences
#n is the number of sentences to summarize whole webpage too
    from heapq import nlargest
    sents_idx = nlargest(n, sentenceValue, key=sentenceValue.get)
    return [sentences[j] for j in sents_idx]


someUrl = "https://www.washingtonpost.com/news/the-switch/wp/2015/08/06/why-kids-are-meeting-more-strangers-online-than-ever-before/"
#someUrl="https://www.nytimes.com/2017/05/08/technology/uk-election-facebook-fake-news.html"
#someUrl="https://fivethirtyeight.com/features/the-worst-tweeter-in-politics-isnt-trump/"

# the article we would like to summarize
textOfUrl = get_only_text_washington_post_url(someUrl)
    
count=Counter(cleanText(textOfUrl[1]))
count.most_common(5)

summary= summarize(textOfUrl[1],5)
print (textOfUrl[0])
print(summary)