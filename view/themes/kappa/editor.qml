import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Basic

Item {
	width: parent.width
	height: parent.height
	x: 0
	y: 0

	id: root
	property QtObject backend: parent.backend
	property QtObject controller: parent.backend.editor

	signal loadHome

	readonly property int navbar_size: 70
	readonly property int menu_size: 500
	readonly property int editor_size: width - menu_size - 200 - 20

	Connections {
		target: root.controller

		function onEditorLoadCards(cards) {
			
		}

		function onAppExitEditor() {
			root.loadHome()
		}
	}

	// Full Screen
	Rectangle {
		anchors.fill: parent

		Rectangle {
			width: parent.width
			height: root.navbar_size
			x: 0
			y: 0
			color: "#8e59ea"

			Button {
				width: 100
				height: parent.height * 0.8
				x: 100
				y: parent.height * 0.1

				onClicked: root.controller.exitEditor()

				Text {
					anchors.fill: parent
					text: "Back"
					font.family: "Noto Sans JP Regular"
					font.pointSize: 20
					color: "#888888"

					horizontalAlignment: TextInput.AlignHCenter
					verticalAlignment: TextInput.AlignVCenter
				}
			}
		}

		Rectangle {
			x: 0
			y: root.navbar_size
			width: parent.width
			height: parent.height - root.navbar_size
			color: "#CCCCCC"

			// Selection
			Rectangle {
				width: root.menu_size
				height: parent.height * 0.9
				x: 100
				y: parent.height * 0.05

				radius: 0
				border.color: "#8e59ea"
				border.width: 1


				ListView {
					id: card_list
					width: parent.width - 2
					height: parent.height - 2
					x: 1
					y: 1

					clip: true
					model: controller.editorModel
					highlight: Rectangle { color: "lightBlue" }
					
					delegate: Item {
						width: card_list.width
						height: 40

						Text {
							id: questionText
							width: parent.width - 20
							height: parent.height - 20
							x: 10
							y: 10

							text: `${question} : ${meaning[0]} / ${onyomi[0]} / ${kunyomi[0]}`
							font.family: "Noto Sans JP Regular"
							font.pointSize: 20
							color: "#222222"

							horizontalAlignment: TextInput.AlignLeft
							verticalAlignment: TextInput.AlignVCenter
						}

						MouseArea {
							id: listDelegateMouseArea
							anchors.fill: parent
							hoverEnabled: true
							onClicked: {
								controller.editorButtonClicked(index)
								card_list.currentIndex = index
							}
						}
					}
				}
			}

			// Editor
			Rectangle {
				id: editor_panel

				readonly property int label_size: 150

				width: root.editor_size
				height: parent.height * 0.9
				x: root.menu_size + 100 + 20
				y: parent.height * 0.05

				radius: 0
				border.color: "#8e59ea"
				border.width: 1

				Item {
					width: parent.width - 20
					height: 50
					x: 10
					y: 0

					Text {
						width: editor_panel.label_size

						anchors.fill: parent
						text: "Question:"
						font.family: "Noto Sans JP Regular"
						font.pointSize: 20
						color: "#222222"

						horizontalAlignment: TextInput.AlignLeft
						verticalAlignment: TextInput.AlignVCenter
					}

					TextField {
						height: parent.height * 0.8
						width: parent.width - editor_panel.label_size
						x: editor_panel.label_size
						y: parent.height * 0.1

						placeholderText: ""
						text: ""
						focus: true
						font.family: "Noto Sans JP Regular"
						font.pointSize: 18
					}
				}
			}
		}
	}
}