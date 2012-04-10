/*
Copyright (C) 2012 Riccardo Ferrazzo <f.riccardo87@gmail.com>

This file is part of TwitterCrawler.

    TwitterCrawler is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TwitterCrawler is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with TwitterCrawler.  If not, see <http://www.gnu.org/licenses/>

*/

// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1
import QtMobility.location 1.2

import "MainView.js" as UT

View{
    id: mainView
    property bool mapEnabled: true
    signal newSearch()
    signal stopSearch()
    signal startMapSearch(variant lat1, variant long1, variant lat2, variant long2)
    signal startContentSearch(string content)
    signal requestPointInfo(variant points)
    signal linkClicked(string url)
    signal hashClicked(variant hash)
    function showPointInfo(info){
        UT.showPointInfo(info)
    }
    function showOnlyDots(ids){
        UT.showOnlyDots(ids)
    }
    function addMapObject(id, lat, lon){
        var component = Qt.createComponent("MapDot.qml");
        var object = component.createObject(map, {dbId:id, latitude:lat, longitude: lon});
        map.addMapObject(object);
        UT.locations.push(object);
        if (object == null) {
            console.log("Error creating object");
        }
    }
    Component.onCompleted: {
        UT.root = mainView;
        UT.map = map;
        UT.toolBaloon = info;
        UT.infoBaloon = pointInfo;
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
                focus = true;
                if(clickNumber < 1 && !map.enabled){
                    if(clickNumber == 0){
                        selectedRegion.topLeft = mouse.coordinate
                        selectedRegion.bottomRight = mouse.coordinate
                    }
                    clickNumber++;
                } else {
                    clickNumber = 0;
                }
                var selectedIcon = UT.selectMarkerIcon(mouse.x, mouse.y);

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
    ToolBaloon{
        id: pointInfo
        visible: false
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: info.left
        anchors.margins: 5
    }

    Keys.onPressed: {
        if (event.key == Qt.Key_Plus) {
            map.zoomLevel += 1
        } else if (event.key == Qt.Key_Minus) {
            map.zoomLevel -= 1
        }
    }
}
