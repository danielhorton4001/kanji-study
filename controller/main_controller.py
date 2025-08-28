from PySide6.QtCore import QObject, Property

from controller.review_controller import ReviewController



class AppController(QObject):
	""""""

	def __init__(self, _app):
		super().__init__()
		self.app = _app

		self.review_controller = ReviewController(self.app, self)


	@Property(QObject, constant=True)
	def review(self):
		return self.review_controller