# Imports
import json
import requests
import datetime
from jaconv import hira2kata, kata2hira
import random
from pathlib import Path

# Constants
MEANING	= 'meanings'
KUNYOMI	= 'kun_readings'
ONYOMI	= 'on_readings'
LABELS	= {
	MEANING: "Meaning", KUNYOMI: "Reading", ONYOMI: "Vocabulary"
}
SRS_EASE_FACTOR = 2.2
USER_DECK_DIR = "userdata/deck.json"



class Deck:
	""""""

	def __init__(self, kanji_json, save_dir):
		self.kanji = kanji_json
		self.keys = self.kanji.keys()
		self.decodeSrs()
		self.save_dir = save_dir


	def saveToFile(self, filedir=None):
		if filedir == None: filedir = self.save_dir
		self.encodeSrs()
		with open(filedir, 'w', encoding='utf-8') as f:
			json.dump(self.kanji, f, ensure_ascii=False, indent=4)
		self.decodeSrs()


	# 
	def getKanji(self, kanji):
		return self.kanji[kanji]


	def _getFirstKanji(self):
		return list(self.keys)[0]


	# General setters
	def _appendValue(self, kanji, k, v):
		self.kanji[kanji][k].append(v)
	

	def _setValue(self, kanji, k, v):
		self.kanji[kanji][k] = v


	# Meaning setters
	def addMeaning(self, kanji, meaning):
		self._appendValue(kanji, MEANING, meaning)


	def setMeanings(self, kanji, meanings):
		self._setValue(kanji, MEANING, meanings)


	# Kunyomi setters
	def addKunyomi(self, kanji, reading):
		self._appendValue(kanji, KUNYOMI, reading)


	def setKunyomi(self, kanji, readings):
		self._setValue(kanji, KUNYOMI, readings)


	# Onyomi setters
	def addOnyomi(self, kanji, reading):
		self._appendValue(kanji, ONYOMI, reading)


	def setOnyomi(self, kanji, readings):
		self._setValue(kanji, ONYOMI, readings)
	

	# SRS getters and setters
	def decodeSrs(self):
		for kanji in self.keys:
			srs_str = self.kanji[kanji]['srs']		# eg. "0|2025-01-20,0|2025-01-20,0|2025-01-20"
			srs_cat = srs_str.split(",")
			srs_sep = []
			for cat in srs_cat:
				srs_sep.append( cat.split("|") )
			srs_dict = {
				MEANING: {'stage': int(srs_sep[0][0]), 'next_rep_date': datetime.datetime.strptime(srs_sep[0][1],'%Y-%m-%d').date()},
				KUNYOMI: {'stage': int(srs_sep[1][0]), 'next_rep_date': datetime.datetime.strptime(srs_sep[1][1],'%Y-%m-%d').date()},
				ONYOMI: {'stage': int(srs_sep[2][0]), 'next_rep_date': datetime.datetime.strptime(srs_sep[2][1],'%Y-%m-%d').date()},
			}
			self.kanji[kanji]['srs'] = srs_dict


	def encodeSrs(self):
		for kanji in self.keys:
			srs_dict = self.kanji[kanji]['srs']
			srs = "{}|{},{}|{},{}|{}".format(
				str(srs_dict[MEANING]['stage']), str(srs_dict[MEANING]['next_rep_date']),
				str(srs_dict[KUNYOMI]['stage']), str(srs_dict[KUNYOMI]['next_rep_date']),
				str(srs_dict[ONYOMI]['stage']), str(srs_dict[ONYOMI]['next_rep_date']),
			)
			self.kanji[kanji]['srs'] = srs
	

	def changeSrsStage(self, kanji, category, stage=1):
		new_stage = max(0, self.kanji[kanji]['srs'][category]['stage'] + stage)
		self.kanji[kanji]['srs'][category]['stage'] = new_stage
		
		new_date = self.calcNextRepDate(new_stage)
		self.kanji[kanji]['srs'][category]['next_rep_date'] = new_date


	def calcNextRepDate(self, stage):
		return (datetime.date.today() + datetime.timedelta(days=self.calcDaysToNextRep(stage))).strftime('%Y-%m-%d')
	

	def calcDaysToNextRep(self, stage):
		if stage > 3: return round(SRS_EASE_FACTOR * self.calcDaysToNextRep(stage-1))
		if stage == 3: return 7
		if stage == 2: return 3
		if stage == 1: return 1
		return 0



class ReviewDeck:
	""""""

	def __init__(self, deck):
		self.deck = deck
		self.cards = []
		self.shuffleReviewDeck()


	def shuffleReviewDeck(self, limit=10):
		self.cards = []
		for kanji in self.deck.keys:
			q = kanji
			srs = self.deck.kanji[kanji]['srs']
			today = datetime.date.today()
			m, k, o = self.deck.kanji[kanji][MEANING], self.deck.kanji[kanji][KUNYOMI], self.deck.kanji[kanji][ONYOMI]
			if m != [] and srs[MEANING]['next_rep_date'] <= today:
				self.cards.append( ReviewCard(q, MEANING, self.deck.kanji[kanji][MEANING]) )
			if k != [] and srs[KUNYOMI]['next_rep_date'] <= today:
				self.cards.append( ReviewCard(q, KUNYOMI, self.deck.kanji[kanji][KUNYOMI]) )
			if o != [] and srs[ONYOMI]['next_rep_date'] <= today:
				self.cards.append( ReviewCard(q, ONYOMI, self.deck.kanji[kanji][ONYOMI]) )
		random.shuffle(self.cards)
		if len(self.cards) > limit:
			self.cards = self.cards[0:limit]
		return len(self.cards) > 0


	@property
	def cur_card(self):
		if len(self.cards) == 0: return None
		return self.cards[0]


	@property
	def current_question(self):
		if len(self.cards) == 0: return None
		return self.cur_card.question


	@property
	def current_mode(self):
		if len(self.cards) == 0: return None
		return self.cur_card.category


	def startReview(self):
		self.shuffleReviewDeck()
		return self.nextCard()


	def isAnswerCorrect(self, answer):
		return self.cur_card.isAnswerCorrect(answer)


	def isAnswerIncorrect(self, answer):
		kanji = self.deck.kanji[self.current_question]
		mode = self.current_mode

		if mode == ONYOMI:
			kun = kata2hira(answer)
			return not kun in self.fuzzyMeanings(kanji[KUNYOMI])
		
		if mode == KUNYOMI:
			on = hira2kata(answer)
			return not on in self.fuzzyMeanings(kanji[ONYOMI])
		
		return True
	

	def fuzzyMeanings(self, answers):
		new_answers = []
		for answer in answers:
			new_answers.append(answer)
			# okurigana (.)
			if "." in answer:
				new_answers.append( answer.split(".")[0] )
				new_answers.append( answer.replace(".", "") )
			# whatever this is (-)
			if "-" in answer:
				new_answers.append( answer.replace("-", "") )
		return new_answers


	def markCard(self, correct):
		if not self.cur_card.failed:
			direction = 1 if correct else -1
			self.deck.changeSrsStage(self.cur_card.question, self.cur_card.category, stage=direction)
			self.cur_card.failed = True
		if correct:
			self.cards.pop(0)
		else:
			self.skipCard()


	def nextCard(self):
		return len(self.cards) > 0


	def saveDeckToFile(self):
		# TODO: This
		#print("SAVE CALLED")
		self.deck.saveToFile(filedir=None) # saves to deck.save_dir


	def skipCard(self):
		self.cards += [self.cards.pop(0)]


	def generateHint(self, kanji):
		kanji_json = self.deck.kanji[kanji]
		title = kanji
		meanings = kanji_json[MEANING]
		onyomi = kanji_json[ONYOMI]
		kunyomi = kanji_json[KUNYOMI]
		return title, meanings, onyomi, kunyomi



class ReviewCard:
	""""""

	def __init__(self, question, category, answers):
		self.question = question
		self.category = category
		self.answers = answers.copy()

		# make it usable
		for answer in answers:
			# okurigana (.)
			if "." in answer:
				self.answers.append( answer.split(".")[0] )
				self.answers.append( answer.replace(".", "") )
			# whatever this is (-)
			if "-" in answer:
				self.answers.append( answer.replace("-", "") )

		self.failed = False


	def isAnswerCorrect(self, answer):
		if self.category == ONYOMI: answer = hira2kata(answer)
		if self.category == KUNYOMI: answer = kata2hira(answer)
		return answer in self.answers



def initial_api_setup():
	full_api = None
	with open("model/kanjiapi/kanjiapi_full.json", 'r', encoding='utf-8') as f: full_api = json.load(f)
	
	for grade in range(6):
		grade_num = grade + 1
		grade_json =  requests.get("https://kanjiapi.dev/v1/kanji/grade-{}".format(grade_num)).json()
		grade_dict = {}
		for kanji in grade_json:
			grade_dict[kanji] = getKanjiDetails(full_api, kanji)
		with open("model/kanjiapi/grade-{}.json".format(grade_num), 'w', encoding='utf-8') as f: json.dump(grade_dict, f, ensure_ascii=False, indent=4)



def getKanjiDetails(api, kanji):
	kanji_info = api['kanjis'][kanji]

	kanji_dict = {}
	for k in ["kanji", "kun_readings", "on_readings", "meanings"]:
		kanji_dict[k] = kanji_info[k]
	
	today = str( datetime.date.today() )
	kanji_dict['srs'] = "0|" + today + ",0|" + today + ",0|" + today
	
	return kanji_dict



def getGradeDeck(grade):
	deck = None
	with open("model/kanjiapi/grade-{}.json".format(grade), 'r', encoding='utf-8') as f:
		json_dict = json.load(f)
		deck = Deck(json_dict, save_dir=USER_DECK_DIR)
	return deck



def getUserDeck():
	deck = None
	path = Path(USER_DECK_DIR)
	if path.exists():
		with open(USER_DECK_DIR, 'r', encoding='utf-8') as f:
			json_dict = json.load(f)
			deck = Deck(json_dict, save_dir=USER_DECK_DIR)
	else:
		# If we don't have a userdeck, generate a copy of grade-1.json
		deck = getGradeDeck(1)
	return deck



if __name__ == "__main__":
	initial_api_setup()