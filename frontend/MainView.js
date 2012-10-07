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

var locations = new Array();
var tracks = new Object();
var newSearchIndex = -1;
var searchGroup = -1;
var lastselected = -1;
var unlocatedTweets = -1;
var root;
var map;
var toolBaloon;
var selectedRegion;
var historicalMenu;

function setTools(){
    newSearchIndex = toolBaloon.addElement("ToolButton.qml", "newSearch", {text: qsTr("New Search")}, -1);
    setNewSearchButton();
}

function setNewSearchButton(){
    if(newSearchIndex == -1)
        return;
    var el = toolBaloon.getElement(newSearchIndex);
    el.clicked.connect(function(){
                           newSearch();
                       });
}

function newSearch(){
    toolBaloon.empty();
    root.clearTweets();
    emptyMap();
    locations = new Array();
    unlocatedTweets = -1;
    var radio = toolBaloon.addElement("SearchMenu.qml", "search", {}, -1);
    var el = toolBaloon.getElement(radio);
    el.searchContentChanged.connect(function(value){
                                        if(searchGroup != -1){
                                            toolBaloon.deleteGroup(searchGroup);
                                        }
                                        searchGroup = toolBaloon.addGroup();
                                        var group = toolBaloon.getElement(searchGroup);
                                        switch(value){
                                        case 1:
                                            var selectArea = toolBaloon.addElement("ToolButton.qml", "mapBlock", {text: qsTr("Select area"), checkable: true}, searchGroup);
                                            group[selectArea].clicked.connect(function(){
                                                                                  root.mapEnabled = !group[selectArea].checked;
                                                                              });
                                            var startSearch = toolBaloon.addElement("ToolButton.qml", "ssearch", {text: qsTr("Start search")}, searchGroup);
                                            group[startSearch].clicked.connect(function(){
                                                                                   if(group[selectArea].checked)
                                                                                        group[selectArea].clicked("");
                                                                                   switch(el.searchType){
                                                                                   case 1:
                                                                                       root.startHistoricalMapSearch(selectedRegion.topLeft.latitude,
                                                                                                                     selectedRegion.topLeft.longitude,
                                                                                                                     selectedRegion.bottomRight.latitude,
                                                                                                                     selectedRegion.bottomRight.longitude, root.historicalSearchDelay);
                                                                                       showSearchInterface("rest", "")
                                                                                       break;
                                                                                   case 2:
                                                                                       root.startRealtimeMapSearch(selectedRegion.topLeft.latitude,
                                                                                                           selectedRegion.topLeft.longitude,
                                                                                                           selectedRegion.bottomRight.latitude,
                                                                                                           selectedRegion.bottomRight.longitude);
                                                                                       showSearchInterface("streaming", "")
                                                                                       break;
                                                                                   }
                                                                               });
                                            break;
                                        case 2:
                                            var txt = toolBaloon.addElement("ToolInput.qml", "txt", {}, searchGroup);
                                            var startSearch = toolBaloon.addElement("ToolButton.qml", "ssearch", {text: qsTr("Start search")}, searchGroup);
                                            group[startSearch].clicked.connect(function(){
                                                                                   switch(el.searchType){
                                                                                   case 1:
                                                                                       root.startHistoricalContentSearch(group[txt].text, root.historicalSearchDelay);
                                                                                       showSearchInterface("rest", group[txt].text);
                                                                                       break;
                                                                                   case 2:
                                                                                       root.startRealtimeContentSearch(group[txt].text);
                                                                                       showSearchInterface("streaming", group[txt].text);
                                                                                       break;
                                                                                   }
                                                                               });
                                            break;
                                        }
                                    });
    el.searchTypeChanged.connect(function(){
                                     switch(el.searchType){
                                     case 1:
                                         historicalMenu.visible = true;
                                         break;
                                     case 2:
                                         historicalMenu.visible = false;
                                         break;
                                     }
                                 });
}

function showSearchInterface(type, word){
    toolBaloon.empty();
    historicalMenu.visible = false;
    var title = toolBaloon.addElement("ToolText.qml", "info", {text: qsTr("Searching %1").arg(word), "font.bold": true}, -1);
    var titleEl = toolBaloon.getElement(title);
    switch(type){
    case "rest":
        var addPageIdx = toolBaloon.addElement("ToolButton.qml", "newStep", {text: qsTr("More results")}, -1);
        var addPage = toolBaloon.getElement(addPageIdx);
        addPage.clicked.connect(function(){
                                    root.addPage();
                                })
        break;
    case "streaming":
        var stopSearch = toolBaloon.addElement("ToolButton.qml", "stop", {text: qsTr("Stop")}, -1);
        var el = toolBaloon.getElement(stopSearch);
        el.clicked.connect(function(){
                               root.stopSearch();
                               titleEl.text = qsTr("Done")
                           });
        var realtimeTrack = toolBaloon.getElement(toolBaloon.addElement("ToolButton.qml", "realtimetrack", {text: qsTr("Realtime track"), checkable: true}, -1));
        realtimeTrack.clicked.connect(function(){
                                          root.realtimeTrack = realtimeTrack.checked;
                                      });
        break;
    }
    var saveSearch = toolBaloon.getElement(toolBaloon.addElement("ToolButton.qml", "save", {text:qsTr("Save results")}, -1));
    saveSearch.clicked.connect(function(){
                                   root.saveSearch();
                               });
    newSearchIndex = toolBaloon.addElement("ToolButton.qml", "newSearch", {text: qsTr("New search")}, -1);
    var el = toolBaloon.getElement(newSearchIndex);
    el.clicked.connect(function(){
                           if(type == "streaming")
                               root.stopSearch();
                           newSearch();
                       });
}

function emptyMap(){
    for(var i in tracks){
        map.removeMapObject(tracks[i]);
    }
    for(var i=locations.length-1; i>=0; i--){
        map.removeMapObject(locations[i]);
    }
    selectedRegion.topLeft.latitude = 0;
    selectedRegion.topLeft.longitude = 0;
    selectedRegion.bottomRight.latitude = 0;
    selectedRegion.bottomRight.longitude = 0;
    map.pan(0,0);
}

function selectMarkerIcon(mx, my){
    root.clearTweetList();
    var res = new Array();
    var sel = -1;
    for(var i = (UT.locations.length-1); i >= 0; --i) {
        var topLeftPoint = map.toScreenPosition(locations[i].coordinate);

        var xStart = parseInt(topLeftPoint.x-12);
        var yStart =  parseInt(topLeftPoint.y-12);
        var xsizes = 24;

        if((mx >= xStart) && (my >= yStart)
                && (mx <= (xStart + xsizes)) && (my <= (yStart + xsizes))){
            root.addTweetToList(locations[i].arrayIndex);
            res.push(i);
        }
    }
    if(res.length == 0){
        root.clearTweetList();
        return -1;
    }
    return res[0];
}

function addUntrackedTweet(number){
    if(unlocatedTweets == -1){
        toolBaloon.addElement("ToolText.qml", "title", {text: "Unlocalized tweets:"}, -1)
        unlocatedTweets = toolBaloon.addElement("ToolButton.qml", "untracked", {text: number}, -1);
        var bt = toolBaloon.getElement(unlocatedTweets);
        bt.clicked.connect(function(){
                               root.showUnlocatedTweets();
                           });
        return;
    }
    var btn = toolBaloon.getElement(unlocatedTweets);
    btn.text = number;
}

function error(message){
    toolBaloon.addElement("ToolText.qml", "error", {text: "<b color=red>Error:</b> "+message}, -1);
}
