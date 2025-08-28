import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from controller.main_controller import AppController



if __name__ == "__main__":
	# Main Window (the view)
	app = QGuiApplication(sys.argv)

	# QML Engine
	engine = QQmlApplicationEngine()
	engine.quit.connect(app.quit)
	engine.load("view/main.qml")
	if not engine.rootObjects():
		sys.exit(-1)

	# Create controller instance
	controller = AppController(app)

	# Pass controller for passing data to QML
	engine.rootObjects()[0].setProperty('controller', controller)

	# Exit
	exit_code = app.exec()
	del engine
	sys.exit(exit_code)