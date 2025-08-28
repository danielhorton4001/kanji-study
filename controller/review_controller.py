from PySide6.QtCore import QObject, Signal, Slot, Property

from controller.jpn_keyboard import toHirigana, toKatakana
from model.deck import getGradeDeck, LABELS, MEANING, ONYOMI, KUNYOMI, ReviewDeck



# Review constants
COLOR_TEXT_UNANSWERED	= '#000000'
COLOR_TEXT_ANSWERED		= '#FFFFFF'

COLOR_BG_UNANSWERED		= '#FFFFFF'
COLOR_BG_CORRECT		= '#40d14a'
COLOR_BG_INCORRECT		= '#ff475c'

COLOR_BORDER_UNANSWERED	= '#7aabbc'
COLOR_BORDER_CORRECT	= '#37ad3f'
COLOR_BORDER_INCORRECT	= '#d8384b'



class ReviewController(QObject):

	changeCard = Signal(str, str, arguments=['question','context'])
	updateField = Signal(str, int, arguments=['text', 'cursorPosition'])
	setInputColours = Signal(str, str, str, arguments=['color', 'color_bg', 'color_border'])
	setInputEnabled = Signal(bool, arguments=['enabled'])
	refocus = Signal()
	showHint = Signal(str, str, str, str)
	appExitReview = Signal()


	def __init__(self, app, parent):
		super().__init__()
		self.app = app
		self.backend = parent
		self.deck = ReviewDeck( getGradeDeck(1) )


	def loadCard(self):
		question = self.deck.current_question
		label = LABELS[self.deck.current_mode]

		self.changeCard.emit(question, label)
		self.updateField.emit("", 0)
		self.setInputColours.emit(COLOR_TEXT_UNANSWERED, COLOR_BG_UNANSWERED, COLOR_BORDER_UNANSWERED)
		self.setInputEnabled.emit(True)

		self.last_question = question


	@Slot()
	def onReviewLoaded(self):
		if self.deck.startReview():
			self.loadCard()
			return
		
		# No cards to study, quit review mode
		self.exitReview()

	@Slot(str, int)
	def textChanged(self, text, cursorPosition):
		# Don't swap characters when in Meaning mode
		if self.deck.current_mode == MEANING: return

		# Check for complete characters and convert them
		if self.deck.current_mode == ONYOMI:
			converted_text, new_cursor_position = toKatakana(text, cursorPosition)
		else:
			converted_text, new_cursor_position = toHirigana(text, cursorPosition)
		self.updateField.emit(converted_text, new_cursor_position)
	
	@Slot(str)
	def answerSubmitted(self, text):
		mode = self.deck.current_mode
		question = self.deck.current_question

		# fuzzy answer
		answer = text.lower()
		if mode != MEANING and "n" in answer:
			answer = answer.replace("n", "ん")
			self.updateField.emit(answer, -1)

		if self.deck.isAnswerCorrect(answer):
			# Answer correct
			self.deck.markCard(correct=True)
			self.changeCard.emit(question, LABELS[mode])
			self.setInputColours.emit(COLOR_TEXT_ANSWERED, COLOR_BG_CORRECT, COLOR_BORDER_CORRECT)
			self.setInputEnabled.emit(False)
			return

		if self.deck.isAnswerIncorrect(answer):
			# Answer incorrect
			self.deck.markCard(correct=False)
			self.changeCard.emit(question, LABELS[mode])
			self.setInputColours.emit(COLOR_TEXT_ANSWERED, COLOR_BG_INCORRECT, COLOR_BORDER_INCORRECT)
			self.setInputEnabled.emit(False)
			return

		# Answer is incorrect, but matches an incorrect reading
		if mode == KUNYOMI:
			self.changeCard.emit(question, "(Looking for the kun'yomi reading)")
		if mode == ONYOMI:
			self.changeCard.emit(question, "(Looking for the on'yomi reading)")


	@Slot()
	def nextCard(self):
		if self.deck.nextCard():
			self.loadCard()
			return
		
		# Last card completed
		self.changeCard.emit("", "")
		self.updateField.emit("", 0)
		self.setInputColours.emit(COLOR_TEXT_UNANSWERED, COLOR_BG_UNANSWERED, COLOR_BORDER_UNANSWERED)
		self.setInputEnabled.emit(False)
		self.exitReview()
	
	@Slot()
	def exitReview(self):
		self.deck.saveDeckToFile()
		self.appExitReview.emit()

	@Slot()
	def showCardInfo(self):
		self.refocus.emit()
		title, meanings, onyomi, kunyomi = self.deck.generateHint( self.last_question )
		self.showHint.emit( title, ", ".join(meanings), ", ".join(onyomi), ", ".join(kunyomi) )

	@Slot()
	def skipCard(self):
		self.deck.skipCard()
		self.loadCard()