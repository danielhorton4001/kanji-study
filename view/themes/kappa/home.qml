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

	signal loadReview
	signal loadEditor

	readonly property int navbar_size: 70
	readonly property int menu_size: 500

	Connections {
		target: root.controller
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

				Button {
					id: review_button
					width: parent.width * 0.8
					height: 50
					x: parent.width * 0.1
					y: 50

					onClicked: root.loadReview()

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

						text: "Review"
						font.family: "Noto Sans JP Bold"
						font.pointSize: 10
						color: "#888888"

						horizontalAlignment: TextInput.AlignHCenter
						verticalAlignment: TextInput.AlignVCenter
					}
				}

				Button {
					id: deck_button
					width: parent.width * 0.8
					height: 50
					x: parent.width * 0.1
					y: 50 + 50 + 10

					onClicked: root.loadEditor()

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

						text: "Edit Deck"
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