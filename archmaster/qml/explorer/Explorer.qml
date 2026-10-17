import QtQuick
import QtQuick.Controls


Flickable {
    id: root

    width: parent ? parent.width : 0
    height: parent ? parent.height : 0

    contentWidth: width
    clip: true

    MoveLine {
        id: moves
        width: root.width - 8
        model: game ? game.tree : null
        delegate: MoveDelegate {}
    }

    contentHeight: moves.height

    ScrollBar.vertical: ScrollBar {
        policy: root.contentHeight > root.height ?
            ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
        width: 8

        contentItem: Rectangle {
            color: theme.midlight
        }
    }
}
