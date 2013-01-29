import QtQuick 1.1

View {
    color: "#4E4E4E"
    Column{
        anchors.centerIn: parent
        width: 250
        spacing: 5
        ToolButton{
            text: "Save everything as SQL"
            onClicked: {
                controller.saveSearch(0)
            }
        }
        ToolButton{
            text: "Save selection as CSV"
            onClicked: {
                controller.saveSearch(defaultView.getTrackedUsers())
            }
        }
    }
    ToolBaloon{
        id: tools
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.margins: 5
    }
    Component.onCompleted: {
        var i = tools.addElement("ToolButton.qml", "back", {text: qsTr("Back")}, -1);
        var el = tools.getElement(i);
        el.clicked.connect(function(){rootPage.pop();})
    }
}
