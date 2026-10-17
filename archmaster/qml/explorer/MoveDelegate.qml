
import QtQuick
import Qt.labs.qmlmodels

DelegateChooser {
    id: chooser

    role: "type"

    DelegateChoice {
        roleValue: "move"

        Rectangle {
            id: root
            required property var modelData

            implicitWidth: row.implicitWidth + 14
            implicitHeight: row.implicitHeight + 6

            radius: 4
            color: root.modelData.id === (game ? game.current_node_id : -1)
                ? theme.highlight
                : (mouseArea.containsMouse ? theme.window_hover : "transparent")

            Row {
                id: row

                anchors.centerIn: parent
                spacing: 3

                Text {
                    id: label1

                    text: root.modelData.fm
                    color: root.modelData.id === (game ? game.current_node_id : -1)
                        ? theme.highlightedText_disabled
                        : theme.text_disabled
                }
                Text {
                    id: label2

                    text: root.modelData.san
                    color: root.modelData.id === (game ? game.current_node_id : -1)
                        ? theme.highlightedText
                        : theme.text
                }
            }

            MouseArea {
                id: mouseArea
                anchors.fill: parent
                hoverEnabled: true
                onClicked: game.set_current_node_id(root.modelData.id)
            }
        }
    }

    DelegateChoice {
        roleValue: "move_list"

        Item {
            required property var modelData

            width: parent ? parent.width : 0
            implicitHeight: flow.implicitHeight

            Flow {
                id: flow
                width: parent.width
                spacing: 0
                padding: 4

                Repeater {
                    model: modelData.items
                    delegate: chooser
                }
            }
        }
    }

    DelegateChoice {
        roleValue: "variation"

        Item {
            required property var modelData

            width: parent ? parent.width : 0
            implicitHeight: line.implicitHeight
            height: implicitHeight

            Rectangle {
                anchors {
                    top: parent.top
                    bottom: parent.bottom
                }
                x: 10
                width: parent.width - 14  // (10 + 4)
                color: theme.base
            }
            Rectangle {
                anchors {
                    top: parent.top
                    bottom: parent.bottom
                }
                color: theme.text_disabled
                width: 4
                x: 10
            }

            MoveLine {
                id: line
                width: parent.width
                indent: 16
                model: modelData.items
                delegate: chooser
            }
        }
    }
}
