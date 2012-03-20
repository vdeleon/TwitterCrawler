// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1
import QtMobility.location 1.2


View{
    id: mainView
    signal newSearch()
    function addMenuItem(qml, personalize){
        var component = Qt.createComponent(qml);
        var sprite = component.createObject(clumn, personalize);
        if (sprite == null) {
            // Error Handling
            console.log("Error creating object");
        }
    }
    ToolBaloon{
        id: info
        height: clumn.height+7
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 5
        anchors.topMargin: 5
        Column{
            id: clumn
            anchors.top: info.top
            anchors.right: info.right
            anchors.left: info.left
            anchors.margins: 3
            spacing: 1
            add: Transition{
                NumberAnimation {properties: "opacity"; to: 1; duration: 500; easing.type: Easing.OutQuad }
            }
            move: Transition {
                NumberAnimation {
                    properties: "y"
                    easing.type: Easing.OutQuad
                    duration: 500
                }
            }
            Text{
                color: "white"
                text: "Search: None"
            }
            Text{
                id: step
                color: "white"
                text: "SearchStep: 0"
            }
            ToolButton{
                id: newSearch
                text: "Nuova Ricerca"
                onClicked:{
                    mainView.newSearch();
                    searchOptions.visible = true
                    newSearch.visible = false
                }
            }
            RadioGroup{
                id: radioGroup
                onSelectedValueChanged: {
                }
            }
            Row{
                id: searchOptions
                visible: false
                RadioButton{
                    width: clumn.width/3
                    text: "Mappa"
                    group: radioGroup
                    content: mapMenu
                    value: "MapMenu.qml"
                }
                RadioButton{
                    width: clumn.width/3
                    text: "Hash"
                    group: radioGroup
                    content: hashMenu
                    value: "HashMenu.qml"
                }
                RadioButton{
                    width: clumn.width/3
                    text: "Link"
                    group: radioGroup
                    content: linkMenu
                    value: "LinkMenu.qml"
                }
            }
            MapMenu{
                id: mapMenu
                visible: false
                onMapEnabler: {
                    map.enabled = enabled;
                }
            }
            HashMenu{
                id: hashMenu
                visible: false
            }
            LinkMenu{
                id: linkMenu
                visible: false
            }

            z:4
        }
        Behavior on height {NumberAnimation{duration: 500; easing.type: Easing.OutQuad}}
    }
    Map{
        id: map
        property bool enabled: true
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
            property int clickNumber: 0

            onPressed : {
                if(clickNumber < 1 && !map.enabled){
                    if(clickNumber == 0){
                        selectedRegion.topLeft = mouse.coordinate
                        selectedRegion.bottomRight = mouse.coordinate
                    }
                    clickNumber++;
                } else {
                    clickNumber = 0;
                }

                lastX = mouse.x
                lastY = mouse.y
            }
            onReleased : {
                lastX = -1
                lastY = -1
            }
            onPositionChanged: {
                if(!map.enabled){
                    if(clickNumber == 1){
                        selectedRegion.bottomRight = mouse.coordinate
                    }
                    return;
                }
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
                if(!map.enabled) return;
                map.center = mouse.coordinate
                map.zoomLevel += 1
                lastX = -1
                lastY = -1
            }
        }
        MapRectangle {
            id: selectedRegion
            border.color: "green"
            border.width: 3
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
