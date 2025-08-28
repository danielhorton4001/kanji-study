import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Basic

Item {
	width: parent.width
	height: parent.height
	x: 0
	y: 0

	id: root
	property QtObject controller: parent.controller
	property QtObject review_controller: parent.controller.review

	signal loadHome

	readonly property int question_size: height * 0.3
	readonly property int prompt_size: height * 0.075
	readonly property int input_size: height * 0.075
	readonly property int button_row_size: height * 0.05

	Connections {
		target: root.review_controller

		function onChangeCard(question, context) {
			questionText.text = question
			contextText.text = context
			hint_area.visible = false
		}

		function onUpdateField(text, cursorPosition) {
			answerField.text = text
			answerField.cursorPosition = cursorPosition
		}

		function onSetInputColours(color, color_bg, color_border) {
			answerFieldRectangle.color = color_bg
			answerFieldRectangle.border.color = color_border
			answerField.color = color
		}

		function onSetInputEnabled(enabled) {
			answerField.enabled = enabled
			answerField.focus = enabled
			answerField.parent.focus = !enabled

			hint_button.enabled = !enabled
			skip_button.enabled = enabled
		}

		function onRefocus() {
			if (answerField.enabled) {
				answerField.forceActiveFocus()
			} else {
				answerField.parent.forceActiveFocus()
			}
		}

		function onShowHint(title, meanings, onyomi, kunyomi) {
			hint_area.visible = true
			hintTitle.text = title
			hintMeanings.text = meanings
			hintOnyomi.text = onyomi
			hintKunyomi.text = kunyomi
		}

		function onAppExitReview() {
			root.loadHome()
		}
	}

	// Full Screen
	Rectangle {
		anchors.fill: parent

		//// Background
		//Image {
		//	width: parent.width
		//	height: parent.height
		//	source: "images/bg1.png"
		//	fillMode: Image.Tile
		//}

		//// Background
		Rectangle {
			width: parent.width
			height: parent.height
			color: "#EEEEEE"
		}

		// Question Bar
		Rectangle {
			width: parent.width
			height: root.question_size
			x: 0
			y: 0
			color: "#8e59ea"

			Text {
				id: questionText
				width: parent.width
				height: parent.height
				x: 0
				y: 0

				text: ""
				font.family: "Noto Sans JP Regular"
				font.pointSize: 80
				color: "#ffffff"

				horizontalAlignment: TextInput.AlignHCenter
				verticalAlignment: TextInput.AlignVCenter
			}
		}

		// Context Bar
		Rectangle {
			width: parent.width
			height: root.prompt_size
			x: 0
			y: root.question_size
			color: "#e7e3ea"

			Text {
				id: contextText
				width: parent.width
				height: parent.height
				x: 0
				y: 0

				text: ""
				font.family: "Noto Sans JP Bold"
				font.pointSize: 20
				color: "#000000"

				horizontalAlignment: TextInput.AlignHCenter
				verticalAlignment: TextInput.AlignVCenter
			}
		}

		Rectangle {
			width: parent.width
			height: root.input_size
			x: 0
			y: root.question_size + root.prompt_size

			Keys.enabled: true
			Keys.onPressed: (event)=> {
				if (event.key == Qt.Key_Return) {
					root.review_controller.nextCard()
					event.accepted = true
				}
			}

			TextField {
				id: answerField
				width: parent.width
				height: parent.height
				x: 0
				y: 0

				placeholderText: ""
				text: ""
				focus: true
				font.family: "Noto Sans JP Regular"
				font.pointSize: 20

				horizontalAlignment: TextInput.AlignHCenter
				verticalAlignment: TextInput.AlignVCenter

				background: Rectangle {
					id: answerFieldRectangle
					color: "#FFFFFF"
					border.color: "#333"
					border.width: 1
				}

				onTextChanged: {
					root.review_controller.textChanged(text, cursorPosition)
				}

				Keys.onPressed: (event)=> {
					if (event.key == Qt.Key_Return) {
						if (text != "") {
							root.review_controller.answerSubmitted(text)
						}
						event.accepted = true
					}
				}
			}
		}

		Rectangle {
			width: parent.width
			height: root.button_row_size
			x: 0
			y: root.question_size + root.prompt_size + root.input_size + 10

			readonly property int button_width: parent.width * 0.15
			readonly property int button_row_padding: parent.width * ( 0.12 + 0.15 )
			readonly property int button_gap: ( parent.width - button_width * 3 - button_row_padding * 2 ) / 2
			
			color: "#EEEEEE"

			Button {
				id: exit_button
				width: parent.button_width
				height: parent.height * 0.8
				x: parent.button_row_padding
				y: parent.height * 0.1

				onClicked: root.review_controller.exitReview()

				background: Rectangle {
					color: "#FFFFFF"
					border.color: "#888888"
					border.width: 1
					radius: 3
				}

				Text {
					width: parent.width
					height: parent.height
					x: 0
					y: 0

					text: "Exit"
					font.family: "Noto Sans JP Bold"
					font.pointSize: 10
					color: "#888888"

					horizontalAlignment: TextInput.AlignHCenter
					verticalAlignment: TextInput.AlignVCenter
				}
			}
			Button {
				id: hint_button
				width: parent.button_width
				height: parent.height * 0.8
				x: parent.button_row_padding + ( parent.button_width + parent.button_gap ) * 1
				y: parent.height * 0.1

				onClicked: root.review_controller.showCardInfo()

				background: Rectangle {
					color: "#FFFFFF"
					border.color: "#888888"
					border.width: 1
					radius: 3
				}

				Text {
					width: parent.width
					height: parent.height
					x: 0
					y: 0

					text: "Hint"
					font.family: "Noto Sans JP Bold"
					font.pointSize: 10
					color: "#888888"

					horizontalAlignment: TextInput.AlignHCenter
					verticalAlignment: TextInput.AlignVCenter
				}
			}
			Button {
				id: skip_button
				width: parent.button_width
				height: parent.height * 0.8
				x: parent.button_row_padding + ( parent.button_width + parent.button_gap ) * 2
				y: parent.height * 0.1

				onClicked: root.review_controller.skipCard()

				background: Rectangle {
					color: "#FFFFFF"
					border.color: "#888888"
					border.width: 1
					radius: 3
				}

				Text {
					width: parent.width
					height: parent.height
					x: 0
					y: 0

					text: "Skip"
					font.family: "Noto Sans JP Bold"
					font.pointSize: 10
					color: "#888888"

					horizontalAlignment: TextInput.AlignHCenter
					verticalAlignment: TextInput.AlignVCenter
				}
			}
		}

		Rectangle {
			id: hint_area
			x: parent.width * 0.27
			y: root.question_size + root.prompt_size + root.input_size + 10 + root.button_row_size + 10
			width: parent.width * 0.46
			height: parent.height - y - 10
			
			color: "#FFFFFF"
			border.color: "#DDDDDD"
			border.width: 1
			radius: 5
			visible: false

			Text {
				id: hintTitle
				width: parent.width - 50
				height: 100
				x: 25
				y: 10

				text: ""
				font.family: "Noto Sans JP Regular"
				font.pointSize: 40
				color: "#000000"

				horizontalAlignment: TextInput.AlignLeft
				verticalAlignment: TextInput.AlignTop
			}

			Text {
				id: hintMeanings
				width: parent.width - 50
				height: 50
				x: 25
				y: 10 + 100

				text: ""
				font.family: "Noto Sans JP Regular"
				font.pointSize: 20
				color: "#000000"

				horizontalAlignment: TextInput.AlignLeft
				verticalAlignment: TextInput.AlignTop
			}

			Text {
				id: hintOnyomi
				width: parent.width - 50
				height: 50
				x: 25
				y: 10 + 150

				text: ""
				font.family: "Noto Sans JP Regular"
				font.pointSize: 20
				color: "#000000"

				horizontalAlignment: TextInput.AlignLeft
				verticalAlignment: TextInput.AlignTop
			}

			Text {
				id: hintKunyomi
				width: parent.width - 50
				height: 50
				x: 25
				y: 10 + 200

				text: ""
				font.family: "Noto Sans JP Regular"
				font.pointSize: 20
				color: "#000000"

				horizontalAlignment: TextInput.AlignLeft
				verticalAlignment: TextInput.AlignTop
			}
		}
	}

}