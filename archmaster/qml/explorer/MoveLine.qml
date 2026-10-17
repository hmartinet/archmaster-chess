import QtQuick

Item {
    id: root

    property var model: []
    property Component delegate: Item {}
    property int indent: 0

    implicitHeight: content.implicitHeight
    height: implicitHeight

    Column {
        id: content

        x: root.indent
        width: root.width - root.indent
        spacing: 4

        Repeater {
            model: root.model
            delegate: root.delegate
        }
    }
}
