from jaconv import hira2kata, kata2hira



characters = {
	'last': {
		'a': 'あ', 'i': 'い', 'u': 'う', 'e': 'え', 'o': 'お',
		'-': 'ー'
	},
	'mid': {
		'ka': 'か', 'ki': 'き', 'ku': 'く', 'ke': 'け', 'ko': 'こ',
		'ca': 'か', 'ci': 'き', 'cu': 'く', 'ce': 'け', 'co': 'こ',
		'sa': 'さ', 'si': 'し', 'shi': 'し', 'su': 'す', 'se': 'せ', 'so': 'そ',
		'ta': 'た', 'ti': 'ち', 'chi': 'ち', 'tu': 'つ', 'tsu': 'つ', 'te': 'て', 'to': 'と',
		'na': 'な', 'ni': 'に', 'nu': 'ぬ', 'ne': 'ね', 'no': 'の', 'nn': 'ん',
		'ha': 'は', 'hi': 'ひ', 'hu': 'ふ', 'fu': 'ふ', 'he': 'へ', 'ho': 'ほ',
		'ma': 'ま', 'mi': 'み', 'mu': 'む', 'me': 'め', 'mo': 'も',
		'ya': 'や', 'yu': 'ゆ', 'yo': 'よ',
		'ra': 'ら', 'ri': 'り', 'ru': 'る', 're': 'れ', 'ro': 'ろ',
		'wa': 'わ', 'wo': 'を',

		'ga': 'が', 'gi': 'ぎ', 'gu': 'ぐ', 'ge': 'げ', 'go': 'ご',
		'za': 'ざ', 'zi': 'じ', 'ji': 'じ', 'zu': 'ず', 'ze': 'ぜ', 'zo': 'ぞ',
		'da': 'だ', 'di': 'ぢ', 'du': 'づ', 'de': 'で', 'do': 'ど',
		'ba': 'ば', 'bi': 'び', 'bu': 'ぶ', 'be': 'べ', 'bo': 'ぼ',
		'pa': 'ぱ', 'pi': 'ぴ', 'pu': 'ぷ', 'pe': 'ぺ', 'po': 'ぽ'
	},
	'first': {
		'kya': 'きゃ', 'kyu': 'きゅ', 'kyo': 'きょ',
		'cya': 'きゃ', 'cyu': 'きゅ', 'cyo': 'きょ',
		'sha': 'しゃ', 'shu': 'しゅ', 'sho': 'しょ',
		'cha': 'ちゃ', 'chu': 'ちゅ', 'cho': 'ちょ',
		'nya': 'にゃ', 'nyu': 'にゅ', 'nyo': 'にょ',
		'hya': 'ひゃ', 'hyu': 'ひゅ', 'hyo': 'ひょ',
		'mya': 'みゃ', 'myu': 'みゅ', 'myo': 'みょ',
		'rya': 'りゃ', 'ryu': 'りゅ', 'ryo': 'りょ',
		'gya': 'ぎゃ', 'gyu': 'ぎゅ', 'gyo': 'ぎょ',
		'jya': 'じゃ', 'jyu': 'じゅ', 'jyo': 'じょ', 'ja': 'じゃ', 'ju': 'じゅ', 'jo': 'じょ',
		'dya': 'ぢゃ', 'dyu': 'ぢゅ', 'dyo': 'ぢょ',
		'bya': 'びゃ', 'byu': 'びゅ', 'byo': 'びょ',
		'pya': 'ぴゃ', 'pyu': 'ぴゅ', 'pyo': 'ぴょ',
	},
	'firster': {
		'kk': 'っk',
		'ck': 'っk',
		'cc': 'っc',
		'ss': 'っs',
		'tt': 'っt',
		'pp': 'っp',
	}
}

def toHirigana(text, cursorPosition):
	
	for char in characters['firster']:
		text, cursorPosition = findToken(char, 'firster', text, cursorPosition)
	for char in characters['first']:
		text, cursorPosition = findToken(char, 'first', text, cursorPosition)
	for char in characters['mid']:
		text, cursorPosition = findToken(char, 'mid', text, cursorPosition)
	for char in characters['last']:
		text, cursorPosition = findToken(char, 'last', text, cursorPosition)

	return text, cursorPosition

def toKatakana(text, cursorPosition):
	text, cursorPosition = toHirigana(text, cursorPosition)
	return hira2kata(text), cursorPosition

def findToken(token, set, text, cursorPosition):
	found = text.find(token)
	if found == -1: return text, cursorPosition
	text = text.replace(token, characters[set][token])
	cursorPosition += len(characters[set][token]) - len(token)
	return text, cursorPosition

def fuzzyMeanings(answers):
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

if __name__ == "__main__":
	MEANING	= 'meanings'
	KUNYOMI	= 'kun_readings'
	ONYOMI	= 'on_readings'

	answer = "モリ"
	kanji = {
		"kanji": "森",
		"kun_readings": [
			"もり"
		],
		"on_readings": [
			"シン"
		],
		"meanings": [
			"forest",
			"woods"
		],
		"srs": "0|2025-01-21,0|2025-01-21,0|2025-01-21"
	}
	mode = ONYOMI

	if mode == ONYOMI:
		kun = kata2hira(answer)
		print( kun in fuzzyMeanings( kanji[KUNYOMI] ) )
	
	if mode == KUNYOMI:
		kun = kata2hira(answer)
		print( kun in kanji[ONYOMI] )
	
