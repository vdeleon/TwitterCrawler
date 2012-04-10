// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Item {
    id: button
    signal clicked(string value)
    property string text: "ClickMe"
    property bool checkable: false
    property bool checked: false
    property string value: ""
    width: Math.max(244, (text.width+6))
    height: 30
    onClicked: {
        if(checkable){
            checked = !checked;
            if(checked)
                buttonColor.color = "#fff";
            else
                buttonColor.color = "#000";
        }
    }
    Rectangle{
        id: buttonColor
        color: "#000"
        opacity: 0.4
        anchors.fill: parent
        MouseArea{
            anchors.fill: parent
            onPressed: {
                buttonColor.color = "#fff"
            }
            onReleased: {
                buttonColor.color = "#000"
            }
            onClicked: {
                button.clicked(button.value);
            }
        }
    }
    Text{
        id: text
        anchors.centerIn: parent
        color: "#fff"
        text: button.text
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }
}
