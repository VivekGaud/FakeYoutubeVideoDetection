import pickle
import nltk
import sys
import nltk
import sklearn
import pandas
import numpy

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize
df = pd.read_csv('./smallDataset.csv',encoding = "utf-8")

classes = df['label']
encoder = LabelEncoder()
Y = encoder.fit_transform(classes)

text_messages = df['comments'].fillna("")
processed = text_messages.str.lower()


stop_words = set(stopwords.words('english'))

processed = processed.apply(lambda x: ' '.join(
    term for term in x.split() if term not in stop_words))

ps = nltk.PorterStemmer()

processed = processed.apply(lambda x: ' '.join(
    ps.stem(term) for term in x.split()))


# create bag-of-words
all_words = []

for message in processed:
    words = word_tokenize(message)
    for w in words:
        all_words.append(w)
        
all_words = nltk.FreqDist(all_words)

print('Number of words: {}'.format(len(all_words)))
print('Most common words: {}'.format(all_words.most_common(15)))

word_features = list(all_words.keys())[:200]

def find_features(message):
    words = word_tokenize(message)
    features = {}
    for word in word_features:
        features[word] = (word in words)

    return features


# filename = 'final_model.sav'

# loaded_model = pickle.load(open(filename, 'rb'))
# li = ['why are u click bait','fake hai video','nice video but not working','thumbnail is other and video other']
# for i in li:
#     f = find_features(i)
#     print(i ,'--',loaded_model.classify(f))
# result = loaded_model.classify("hgjjb")
# print(result)