# from YTpage.youtubeDetails import video_comments
from YTpage.Vedor_sentiment import Sentiment_by_vedor
from YTpage.comment_scraper import list_of_comments
import time,re,json
from bs4 import BeautifulSoup as bs

from googletrans import Translator
# from translate import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from progress.bar import Bar

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

#load data for find_features
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

# print('Number of words: {}'.format(len(all_words)))
# print('Most common words: {}'.format(all_words.most_common(15)))

word_features = list(all_words.keys())[:200]

filename = 'final_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

def vedor_Result(v_id,comment_count):
	commentsListFiltter = []
	c_count = int(comment_count)
	comments = list_of_comments(v_id,c_count)
	commentsList = []
	# RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
	bad_char ={',','?','&','*','@',':','!','(',')','/','-','#','.',">","<",'_'}
	pos_val =0
	neg_val=0
	comp = 0

	fake_count = 0
	normal_count = 0
	totalCommLimit = 0

	if not comments:
		comments = ['none']
	else:
		pass
	try:
		bar = Bar('Translating:', max=len(comments))
		bar.start()
		translator = Translator(service_urls=['translate.google.co.in'])
		
		file = open("commLimit.txt", "r") 
		totalCommLimit = int(file.read() )
		file.close()

		for c in comments:
			senWithEmoji = c.lower()
			# print(c)
			# print(senWithEmoji)
			if len(c) < 2:
				comments.remove(c)
			# emojiFil = RE_EMOJI.sub(r'', senWithEmoji)
			emojiFil =senWithEmoji.encode('ascii', 'ignore').decode('ascii')
			emojiFil = emojiFil.replace("\n"," ")
			emojiFil = emojiFil.replace("\r","")
			emojiFil = re.sub(r'[0-9]+','',emojiFil)
			emojiFil = re.sub(r'http\S+', '', emojiFil)

			for i in bad_char:
				emojiFil = emojiFil.replace(i,"")
			# print(emojiFil)

			totalCommLimit += len(emojiFil.split())
			with open("commLimit.txt", "w") as f: 
				f.write(str(totalCommLimit)) 
			##Error if used more
			# t = translator.translate(emojiFil).text
			# translator= Translator(to_lang="en")
			# print(totalCommLimit)
			# t = translator.translate(emojiFil).text
			# trans_text = t.lower()
		
			if totalCommLimit <= 10677:
				t = translator.translate(emojiFil).text
				trans_text = t.lower()
				# print("if: ",trans_text)
			else:
				trans_text = emojiFil.lower()
				# print("else: ",trans_text)

			analyser = SentimentIntensityAnalyzer()

			
			score = analyser.polarity_scores(trans_text)
			commentResult = modelResult(trans_text)

			# print(trans_text,'--',commentResult)

			if commentResult == 1:
				fake_count += 1
			else:
				normal_count += 1
			# print(c ,"pos_val -->",score['pos'],"neg_val -->",score['neg'])
			pos_val += score['pos']
			neg_val +=score['neg']
			comp += score['compound']
			bar.next()
		bar.finish()

	except json.decoder.JSONDecodeError:
		print("limit of translator")



	if len(comments) == 0:
		return pos_val,neg_val,comp,fake_count
	else:
			# print("final pos: ",pos_val,"final neg: ",neg_val, "compound", comp)
		finalPosVal = ((pos_val)/len(comments))*100
		finalNegVal = ((neg_val)/len(comments))*100
		finalComp = (comp)/len(comments)
		fakePercent = int((fake_count/len(comments))*100)
		normalPercent = int((normal_count/len(comments))*100)
		# print()
		# print("final pos: ",finalPosVal,"final neg: ",finalNegVal, "compound", finalComp)
		
	return round(finalPosVal,2),round(finalNegVal,2),finalComp,fakePercent,normalPercent


def find_features(message):
    words = word_tokenize(message)
    features = {}
    for word in word_features:
        features[word] = (word in words)

    return features



def modelResult(text):
	feat = find_features(text)
	result = loaded_model.classify(feat)
	return result


