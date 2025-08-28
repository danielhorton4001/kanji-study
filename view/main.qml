import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Basic

ApplicationWindow {
	visible: true
	visibility: Window.Maximized
	width: Screen.desktopAvailableWidth
	height: Screen.desktopAvailableHeight
	x: 0
	y: 0
	flags: Qt.Window
	title: "Home"

	id: root
	property QtObject controller

	Connections {
		target: root.controller
	}

	Loader {
		id: pageloader
		anchors.fill: parent
		
		property bool valid: item != null
		property QtObject controller: root.controller

		source: "themes/kappa/home.qml"

		onLoaded: {
			if (source == "themes/kappa/review.qml") {
				root.controller.review.onReviewLoaded()
			} else if (source == "themes/kappa/editor.qml")
			{
				//root.controller.onEditorLoaded()
			}
		}
	}

	Connections {
		id: listener
		ignoreUnknownSignals: true
		target: pageloader.valid? pageloader.item : null

		function onLoadReview() {
			pageloader.source = "themes/kappa/review.qml"
		}

		function onLoadReviewSelector() {
			pageloader.source = "themes/kappa/review_selector.qml"
		}

		function onLoadEditor() {
			pageloader.source = "themes/kappa/editor.qml"
		}

		function onLoadHome() {
			pageloader.source = "themes/kappa/home.qml"
		}
	}
}