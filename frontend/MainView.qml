// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1
import QtMobility.location 1.2

import "MainView.js" as UT

View{
    id: mainView
    property bool mapEnabled: true
    signal newSearch()
    signal startMapSearch(variant lat1, variant long1, variant lat2, variant long2)
    function addMapObject(id, name, lat, lon){
        var component = Qt.createComponent("MapDot.qml");
        var object = component.createObject(map, {objectName: name, latitude:lat, longitude: lon});
        map.addMapObject(object);
        UT.locations.push(object);
        if (object == null) {
            console.log("Error creating object");
        }
    }
    function selectMarkerIcon(mx, my){
        for(var i = (UT.locations.length-1); i >= 0; --i) {
            var topLeftPoint = map.toScreenPosition(UT.locations[i].coordinate);

            var xStart = parseInt(topLeftPoint.x);
            var yStart =  parseInt(topLeftPoint.y);
            var xsizes = 24;

            if((mx >= xStart) && (my >= yStart)
                    && (mx <= (xStart + xsizes)) && (my <= (yStart + xsizes))){
                UT.getPointInfo(i);
                return i;
            }
        }
        return -1;
    }
    Component.onCompleted: {
        UT.root = mainView;
        UT.map = map;
        UT.toolBaloon = info;
        UT.selectedRegion = selectedRegion
        UT.setTools();
    }
    Map{
        id: map
        property bool enabled: mainView.mapEnabled
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
                var selectedIcon = selectMarkerIcon(mouse.x, mouse.y);

                if(selectedIcon >= 0 && selectedIcon <  UT.locations.length){
                    UT.locations[selectedIcon].source =  "images/map-dot-selected.png";
                }
                if(UT.lastselected != -1)
                    UT.locations[UT.lastselected].source = "images/map-dot.png";
                UT.lastselected = selectedIcon;

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
            topLeft: Coordinate {
                latitude: 0
                longitude: 0
            }
            bottomRight: Coordinate {
                latitude: 0
                longitude: 0
            }
            border.color: "green"
            border.width: 3
        }
    }
    ToolBaloon{
        id: info
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 5
        anchors.topMargin: 5
    }
    Keys.onPressed: {
        if (event.key == Qt.Key_Plus) {
            map.zoomLevel += 1
        } else if (event.key == Qt.Key_Minus) {
            map.zoomLevel -= 1
        }
    }
}
