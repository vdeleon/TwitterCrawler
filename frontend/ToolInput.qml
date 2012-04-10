// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Rectangle{
    id: root
    height: 30
    width: parent.width
    property string text: text.text
    TextInput{
        id: text
        height: 20
        width: parent.width
        anchors.centerIn: parent
        color: "black"
        font.pointSize: 12
        cursorVisible: true
        focus: true
        horizontalAlignment: TextInput.AlignHCenter
    }
}
