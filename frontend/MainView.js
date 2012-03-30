var locations = new Array();
var lastselected = -1;
var newSearchIndex = -1;
var searchGroup = -1;
var root;
var map;
var toolBaloon;
var selectedRegion;

function setTools(){
    newSearchIndex = toolBaloon.addElement("ToolButton.qml", "newSearch", {text: "Nuova Ricerca"}, -1);
    setNewSearchButton();
}

function setNewSearchButton(){
    if(newSearchIndex == -1)
        return;
    var el = toolBaloon.getElement(newSearchIndex);
    el.clicked.connect(function(){
                           newSearch();
                           root.newSearch();
                       })
}

function newSearch(){
    toolBaloon.empty();
    emptyMap();
    newSearchIndex = toolBaloon.addElement("ToolButton.qml", "newSearch", {text: "Nuova Ricerca"}, -1);
    setNewSearchButton();
    var radio = toolBaloon.addElement("SearchMenu.qml", "search", {}, -1);
    var el = toolBaloon.getElement(radio);
    el.selectedValueChanged.connect(function(value){
                                        if(searchGroup != -1){
                                            toolBaloon.deleteGroup(searchGroup);
                                        }
                                        searchGroup = toolBaloon.addGroup();
                                        var group = toolBaloon.getElement(searchGroup);
                                        switch(value){
                                        case 1:
                                            var selectArea = toolBaloon.addElement("ToolButton.qml", "mapBlock", {text: "Seleziona Area", checkable: true}, searchGroup);
                                            group[selectArea].clicked.connect(function(){
                                                                                  root.mapEnabled = group[selectArea].checked;
                                                                              });
                                            var startSearch = toolBaloon.addElement("ToolButton.qml", "ssearch", {text: "Avvia Ricerca"}, searchGroup);
                                            group[startSearch].clicked.connect(function(){
                                                                                   root.startMapSearch(selectedRegion.topLeft.latitude,
                                                                                                       selectedRegion.topLeft.longitude,
                                                                                                       selectedRegion.bottomRight.latitude,
                                                                                                       selectedRegion.bottomRight.longitude);
                                                                                   showSearchInterface();
                                                                               });
                                            break;
                                        case 2:
                                            var startSearch = toolBaloon.addElement("ToolButton.qml", "ssearch", {text: "Avvia Ricerca"}, searchGroup);
                                            group[startSearch].clicked.connect(function(){});
                                            break;
                                        case 3:
                                            var startSearch = toolBaloon.addElement("ToolButton.qml", "ssearch", {text: "Avvia Ricerca"}, searchGroup);
                                            group[startSearch].clicked.connect(function(){});
                                            break;
                                        }
                                    });
}

function showSearchInterface(){
    toolBaloon.empty();
    var title = toolBaloon.addElement("ToolText.qml", "info", {text: "Ricerca in corso"}, -1);
    var stopSearch = toolBaloon.addElement("ToolButton.qml", "stop", {text: "Stop"}, -1);
    var el = toolBaloon.getElement(stopSearch);
    var titleEl = toolBaloon.getElement(title);
    el.clicked.connect(function(){
                           root.stopSearch();
                           titleEl.text = "Ricerca terminata";
                       });
}

function emptyMap(){
    for(var i=locations.length-1; i>=0; i--){
        map.removeMapObject(locations[i]);
    }
    selectedRegion.topLeft.latitude = 0;
    selectedRegion.topLeft.longitude = 0;
    selectedRegion.bottomRight.latitude = 0;
    selectedRegion.bottomRight.longitude = 0;
}

function selectMarkerIcon(mx, my){
    var res = new Array();
    for(var i = (UT.locations.length-1); i >= 0; --i) {
        var topLeftPoint = map.toScreenPosition(UT.locations[i].coordinate);

        var xStart = parseInt(topLeftPoint.x);
        var yStart =  parseInt(topLeftPoint.y);
        var xsizes = 24;

        if((mx >= xStart) && (my >= yStart)
                && (mx <= (xStart + xsizes)) && (my <= (yStart + xsizes))){
            res.push(i);
        }
    }
    if(res.length == 0){
        return -1;
    }
    root.requestPointInfo(res);
    return res[0];
}

function showPointInfo(info){
    root.stopSearch();
    toolBaloon.empty();
    toolBaloon.addElement("ToolText.qml", "element", {text: "Elementi in questo punto: "+info["users"].length}, -1);
    toolBaloon.addElement("ToolText.qml", "ht", {text: "Hashtags utilizzati", "font.bold": true}, -1);
    for(var i in info.hashtags)
        toolBaloon.addElement("ToolText.qml", "h"+i, {text: "#"+info.hashtags[i][1]+" N°:"+info.hashtags[i][0]}, -1);
    toolBaloon.addElement("ToolText.qml", "lt", {text: "Links utilizzati", "font.bold": true}, -1);
    for(var i in info.links)
        toolBaloon.addElement("ToolText.qml", "l"+i, {text: info.links[i][1]+" N°:"+info.links[i][0]}, -1);
}
