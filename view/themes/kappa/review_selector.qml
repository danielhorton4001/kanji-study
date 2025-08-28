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

	signal loadHome
	signal loadReview

	readonly property int navbar_size: 70
	readonly property int menu_size: 500

	Connections {
		target: root.backend
	}

	// Full Screen
	Rectangle {
		anchors.fill: parent

		// Question Bar
		Rectangle {
			width: parent.width
			height: root.navbar_size
			x: 0
			y: 0
			color: "#8e59ea"
		}

		Rectangle {
			x: 0
			y: root.navbar_size
			width: parent.width
			height: parent.height - root.navbar_size
			color: "#CCCCCC"

			Rectangle {
				width: root.menu_size
				height: parent.height * 0.9
				x: (parent.width - root.menu_size) * 0.5
				y: parent.height * 0.05

				radius: 15
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

				Button {
					id: deck_button
					width: parent.width * 0.8
					height: 50
					x: parent.width * 0.1
					y: 50 + 50 + 10

					onClicked: root.loadHome()

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

						text: "Back"
						font.family: "Noto Sans JP Bold"
						font.pointSize: 10
						color: "#888888"

						horizontalAlignment: TextInput.AlignHCenter
						verticalAlignment: TextInput.AlignVCenter
					}
				}
			}
		}
	}

}