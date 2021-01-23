from pages.youtubeDetails import video_comments
from pages.Vedor_sentiment import Sentiment_by_vedor
from pages.comment_scraper import list_of_comments
import time,re,json
from bs4 import BeautifulSoup as bs

from googletrans import Translator
# from translate import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from progress.bar import Bar

def vedor_Result(v_id,comment_count):
	commentsListFiltter = []
	c_count = int(comment_count)
	comments = list_of_comments(v_id,c_count)
	commentsList = []
	# RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
	bad_char ={',','?','&','*','@',':','!','(',')','/','-','#','...'}
	pos_val =0
	neg_val=0
	comp = 0
	words = ["fake","fack","clickbait","click","klicKbait","bait","misleading","missleading","bet"
				,"klikkbat","clickbaited"]
	fake_count = 0

	if not comments:
		comments = ['none']
	else:
		pass
	try:
		bar = Bar('Translating:', max=len(comments))
		bar.start()
		translator = Translator(service_urls=['translate.google.co.in'])
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

			##Error if used more
			# t = translator.translate(emojiFil).text
			# translator= Translator(to_lang="en")
			t = translator.translate(emojiFil).text
			trans_text = t.lower()
			analyser = SentimentIntensityAnalyzer()

			sentence = trans_text.split()
			# print(trans_text)
				# print(sentence)
			for wor in words:
				if wor in sentence:
						# print(wor)
					fake_count += 1
			score = analyser.polarity_scores(trans_text)
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
		# print()
		# print("final pos: ",finalPosVal,"final neg: ",finalNegVal, "compound", finalComp)
		
	return round(finalPosVal,2),round(finalNegVal,2),finalComp,fake_count

	# commentsListFiltter = []
	# c_count = int(comment_count)
	# comments = list_of_comments(v_id,c_count)
	# commentsList = []
	# # RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
	# bad_char ={',','?','&','*','@',':','!','(',')','/','-','#','...'}
	# for c in comments:
	# 	senWithEmoji = c.lower()
	# 	if len(c) < 2:
	# 		comments.remove(c)
	# 	# emojiFil = RE_EMOJI.sub(r'', senWithEmoji)
	# 	emojiFil =senWithEmoji.encode('ascii', 'ignore').decode('ascii')
	# 	emojiFil = emojiFil.replace("\n"," ")
	# 	emojiFil = emojiFil.replace("\r","")
	# 	emojiFil = re.sub(r'[0-9]+','',emojiFil)
	# 	emojiFil = re.sub(r'http\S+', '', emojiFil)

	# 	for i in bad_char:
	# 		emojiFil = emojiFil.replace(i,"")
	# 	commentsList.append(emojiFil)

	# # print(comments)
	# # print(commentsList)
	# # Translate each comments and pass those for sentiment analysis
	# translator = Translator()
	# for comm in commentsList:
	# 	# print(comm)
	# 	trans_text = translator.translate(comm).text
	# 	commentsListFiltter.append(trans_text)
	# 	# time.sleep(1)

	# # Sentiment Result on comments using Vedor sentiment in tuple formet (finalPosVal,finalNegVal,finalComp,fake_count)
	# vedor = Sentiment_by_vedor()
	# vedorResult = vedor.Vedor_sentiment_result(commentsListFiltter)
	# return vedorResult


