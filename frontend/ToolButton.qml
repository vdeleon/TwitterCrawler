// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Item {
    id: button
    signal clicked()
    property string text: "ClickMe"
    property bool checkable: false
    property bool checked: false
    width: parent.width
    height: 30
    Rectangle{
        id: buttonColor
        color: "#000"
        opacity: 0.2
        anchors.fill: parent
        MouseArea{
            anchors.fill: parent
            onPressed: {
                buttonColor.opacity = 0.5
            }
            onReleased: {
                buttonColor.opacity = 0.2
            }
            onClicked: {
                button.clicked();
                if(checkable){
                    checked = !checked;
                    if(checked)
                        buttonColor.opacity = 0.5;
                    else
                        buttonColor.opacity = 0.2;
                }
            }
        }
    }
    Text{
        id: text
        anchors.fill: parent
        color: "#fff"
        text: button.text
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }
}
