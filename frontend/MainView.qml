// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1
import QtMobility.location 1.2
import QtDesktop 0.1

View{
    id: mainView
    ToolBaloon{
        id: info
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 5
        anchors.topMargin: 5
        Column{
            anchors.fill: info
            anchors.margins: 3
            spacing: 1
            Text{
                color: "white"
                text: "Search: None"
            }
            Text{
                id: step
                color: "white"
                text: "SearchStep: 0"
            }
            Button{
                id: btn
                text:"Click"
                onClicked: {
                    step.text="Evvaiiii!"
                }
            }

            z:4
        }
    }
    Map{
        id: map
        anchors.fill: parent
        zoomLevel: 2
        center: Coordinate{
            latitude: 45.6435208
            longitude: 12.6216089
        }
        plugin: Plugin{
            name: "nokia"
        }
        MapMouseArea {
            property int lastX : -1
            property int lastY : -1

            onPressed : {
                lastX = mouse.x
                lastY = mouse.y
            }
            onReleased : {
                lastX = -1
                lastY = -1
            }
            onPositionChanged: {
                if (mouse.button == Qt.LeftButton) {
                    if ((lastX != -1) && (lastY != -1)) {
                        var dx = mouse.x - lastX
                        var dy = mouse.y - lastY
                        map.pan(-dx, -dy)
                    }
                    lastX = mouse.x
                    lastY = mouse.y
                }
            }
            onDoubleClicked: {
                map.center = mouse.coordinate
                map.zoomLevel += 1
                lastX = -1
                lastY = -1
            }
        }
    }
    Keys.onPressed: {
        if (event.key == Qt.Key_Plus) {
            map.zoomLevel += 1
        } else if (event.key == Qt.Key_Minus) {
            map.zoomLevel -= 1
        }
    }
}
