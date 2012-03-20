// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Item {
    id: mapMenu
    width: parent.width
    height: 62
    signal mapEnabler(bool enabled)
        ToolButton{
            id: mapEnabler
            checkable: true
            anchors.top: mapMenu.top
            anchors.left: mapMenu.left
            anchors.right: mapMenu.right
            text: "seleziona area"
            onClicked: {
                mapMenu.mapEnabler(checked);
            }
        }
        ToolButton{
            anchors.top: mapEnabler.bottom
            anchors.left: mapMenu.left
            anchors.right: mapMenu.right
            anchors.topMargin: 2
            text: "Avvia Ricerca"
        }
}
