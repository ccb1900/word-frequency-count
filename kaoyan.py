import collections

import nltk
import redis as rds
from nltk import word_tokenize

pool = rds.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = rds.Redis(connection_pool=pool)


r.delete('words-stats')
r.delete('words-lower')
r.delete('words-upper')
r.delete('words-title')
r.delete('words-unnormal')
r.delete('words-other')
ps = nltk.PorterStemmer()
lemmatizer = nltk.WordNetLemmatizer()
try:
    with open('./ky-1986-2017.txt', 'r') as f:
        tag = word_tokenize(f.read())
        counters = collections.Counter(tag)

        for x in counters:
            # 过滤掉数字
            if x.isdigit():
                continue
            if x.isalpha():
                if x.isupper():
                    r.zincrby('words-upper', x, counters[x])
                elif x.istitle():
                    r.zincrby('words-title', x, counters[x])
                elif x.islower():
                    r.zincrby('words-lower', x, counters[x])
                else:
                    r.zincrby('words-other', x, counters[x])
            else:
                r.zincrby('words-unnormal', x, counters[x])
except LookupError as identifier:
    print("下载语料", identifier)
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')