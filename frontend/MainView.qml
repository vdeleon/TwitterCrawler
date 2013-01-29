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
import "tweets.js" as Tweets

View{
    id: mainView
    property bool mapEnabled: true
    property int historicalSearchDelay: 0
    property bool realtimeTrack: false
    signal stopSearch()
    signal saveSearch();
    signal startRealtimeMapSearch(variant lat1, variant long1, variant lat2, variant long2)
    signal startRealtimeContentSearch(string content)
    signal startHistoricalMapSearch(variant lat1, variant long1, variant lat2, variant long2, int delta)
    signal startHistoricalContentSearch(string content, int delta)
    signal requestPointInfo(variant points)
    signal linkClicked(string url)
    signal hashClicked(variant hash)
    signal addPage()
    function getTrackedUsers(){
        return Object.keys(UT.tracks)
    }

    function refreshPointColor(location, selected){
        if(selected){
            if(UT.tracks[Tweets.getTweetAt(location.arrayIndex).userName] != null)
                location.source = "images/map-dot-tracked-selected.png";
            else{
                location.source = "images/map-dot-selected.png";
            }
        }else{
            if(UT.tracks[Tweets.getTweetAt(location.arrayIndex).userName] != null)
                location.source = "images/map-dot-tracked.png";
            else
                location.source = "images/map-dot.png";
        }
    }
    function showError(message){
        UT.error(message);
    }
    function addTweet(id){
        if(Tweets.getTweetAt(id).location == false){
            UT.addUntrackedTweet(Tweets.getUnlocalizedTweetNumber());
            return;
        }
        var component = Qt.createComponent("MapDot.qml");
        var object = component.createObject(map, {arrayIndex:id});
        map.addMapObject(object);
        UT.locations.push(object);
        var tweet = Tweets.getTweetAt(id)
        if(realtimeTrack && UT.tracks[tweet.userName] != null){
            var coordinate = Qt.createQmlObject("import QtQuick 1.1; import QtMobility.location 1.2;"
                                            +"Coordinate{ latitude: "+ tweet.location.lat+";"
                                            +"longitude: "+tweet.location.lon+"; }", object, "coord");
            UT.tracks[tweet.userName].addCoordinate(coordinate);
            refreshPointColor(object, false);
        }
        if (object == null) {
            console.log("Error creating object");
        }
    }
    function addTrackToMap(id){
        console.log("adding "+id);
        if(UT.tracks[id] != null){
            console.log("   already tracked");
            map.removeMapObject(UT.tracks[id]);
        }
        var object = Qt.createQmlObject("import QtQuick 1.1; import QtMobility.location 1.2;"
                                           +"MapPolyline{ border.color: \"#070785\"; border.width: 2; }",
                                           map, "route");
        map.addMapObject(object);
        UT.tracks[id] = object;
        return object;
    }
    function deleteUserTrack(id){
        console.log("deleting "+id)
        map.removeMapObject(UT.tracks[id])
        UT.tracks[id] = null;
        refreshAllPoints();
    }
    function isTracked(id){
        if(UT.tracks[id] != null){
            return true;
        }
        return false;
    }

    function addTweetToList(arrayIndex){
        tweetList.addItem(Tweets.getTweetAt(arrayIndex));
    }
    function clearTweetList(){
        tweetList.clear();
    }
    function showUnlocatedTweets(){
        var tweets = Tweets.getUnlocalizedTweets();
        for(var i in tweets){
            tweetList.addItem(tweets[i]);
        }
    }
    function clearTweets(){
        Tweets.clearAll();
    }
    function trackUsers(track){
        Tweets.trackingUsers = true;
        Tweets.refreshTracks();
    }
    function refreshAllPoints(){
        for(var i in UT.locations){
            refreshPointColor(UT.locations[i], false);
        }
    }

    Component.onCompleted: {
        UT.root = mainView;
        UT.map = map;
        UT.toolBaloon = info;
        UT.selectedRegion = selectedRegion;
        UT.historicalMenu = historicalMenu
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
                    return;
                } else {
                    clickNumber = 0;
                }
                var selectedIcon = UT.selectMarkerIcon(mouse.x, mouse.y);

                if(selectedIcon >= 0 && selectedIcon <  UT.locations.length){
                    refreshPointColor(UT.locations[selectedIcon], true);
                }
                if(UT.lastselected != -1){
                    refreshPointColor(UT.locations[UT.lastselected], false);
                }

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
    TweetList{
        id: tweetList
        height: mainView.height
        width: 300
    }

    Item{
        id: historicalMenu
        visible: false
        width: 500
        height: 30
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20
        anchors.horizontalCenter: parent.horizontalCenter
        RadioGroup{
            id: historicalGroup
            selectedValue: 0
            onSelectedValueChanged: {
                mainView.historicalSearchDelay = selectedValue;
            }
        }
        Rectangle{
            anchors.fill: parent
            color: "#000"
            opacity: 0.8
            radius: 5
        }
        Row{
            height: parent.height
            anchors.horizontalCenter: parent.horizontalCenter
            RadioButton{
                width: historicalMenu.width/8
                text: "today"
                group: historicalGroup
                value: -1
            }
            RadioButton{
                width: historicalMenu.width/8
                text: "-1 day"
                group: historicalGroup
                value: 0
            }
            RadioButton{
                width: historicalMenu.width/8
                text: "-2 days"
                group: historicalGroup
                value: 1
            }
            RadioButton{
                width: historicalMenu.width/8
                text: "-3 days"
                group: historicalGroup
                value: 2
            }
            RadioButton{
                width: historicalMenu.width/8
                text: "-4 days"
                group: historicalGroup
                value: 3
            }
            RadioButton{
                width: historicalMenu.width/8
                text: "-5 days"
                group: historicalGroup
                value: 4
            }
            RadioButton{
                width: historicalMenu.width/8
                text: "-6 days"
                group: historicalGroup
                value: 5
            }
            RadioButton{
                width: historicalMenu.width/8
                text: "-7 days"
                group: historicalGroup
                value: 6
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
