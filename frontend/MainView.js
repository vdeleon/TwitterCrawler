var locations = new Array();
var selectedElements = new Array();
var lastselected = -1;
var newSearchIndex = -1;
var searchGroup = -1;
var root;
var map;
var toolBaloon;
var infoBaloon;
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
                       });
}

function newSearch(){
    toolBaloon.empty();
    emptyMap();
    lastselected = -1;
    locations = new Array();
    selectedElements = new Array();
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
                                                                                  root.mapEnabled = !group[selectArea].checked;
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
                                            var txt = toolBaloon.addElement("ToolInput.qml", "txt", {}, searchGroup);
                                            var startSearch = toolBaloon.addElement("ToolButton.qml", "ssearch", {text: "Avvia Ricerca"}, searchGroup);
                                            group[startSearch].clicked.connect(function(){
                                                                                   root.startContentSearch(group[txt].text);
                                                                                   showSearchInterface();
                                                                               });
                                            break;
                                        }
                                    });
}

function showSearchInterface(){
    toolBaloon.empty();
    var title = toolBaloon.addElement("ToolText.qml", "info", {text: "Ricerca in corso", "font.bold": true}, -1);
    var stopSearch = toolBaloon.addElement("ToolButton.qml", "stop", {text: "Stop"}, -1);
    var el = toolBaloon.getElement(stopSearch);
    var titleEl = toolBaloon.getElement(title);
    el.clicked.connect(function(){
                           root.stopSearch();
                           titleEl.text = "Ricerca completata"
                       });
    newSearchIndex = toolBaloon.addElement("ToolButton.qml", "newSearch", {text: "Nuova Ricerca"}, -1);
    setNewSearchButton();
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
    var ids = new Array();
    for(var i = (UT.locations.length-1); i >= 0; --i) {
        var topLeftPoint = map.toScreenPosition(locations[i].coordinate);

        var xStart = parseInt(topLeftPoint.x);
        var yStart =  parseInt(topLeftPoint.y);
        var xsizes = 24;

        if((mx >= xStart) && (my >= yStart)
                && (mx <= (xStart + xsizes)) && (my <= (yStart + xsizes))){
            ids.push(locations[i].dbId);
            res.push(i);
        }
    }
    if(res.length == 0){
        infoBaloon.visible = false;
        return -1;
    }
    root.requestPointInfo(ids);
    return res[0];
}

function showAllDots(){
    for(var i in locations)
        locations[i].visible = true;
}

function showOnlyDots(ids){
    //nascondere tutti i punti tranne questi
    for(var i in locations){
        if(findInArray(locations[i].dbId, ids) != -1){
            locations[i].visible = true;
        } else {
            locations[i].visible = false;
        }
    }
}

function findInArray(el, arr){
    for(var i in arr){
        if(arr[i] === el){
            return i;
        }
    }
    return -1;
}

function showPointInfo(info){
    infoBaloon.visible = true;
    infoBaloon.empty();
    infoBaloon.addElement("ToolText.qml", "element", {text: "Elementi in questo punto: "+info["users"].length, "font.bold": true}, -1);
    infoBaloon.addElement("ToolText.qml", "ht", {text: "Hashtags utilizzati", "font.bold": true}, -1);
    var hashIdx = infoBaloon.addElement("ResultFlow.qml", "hash", {}, -1);
    var hashFlow = infoBaloon.getElement(hashIdx);
    for(var i in info.hashtags){
        var idx = hashFlow.addElement("ToolButton.qml", "h"+i, {text: "#"+info.hashtags[i][1]+" N°:"+info.hashtags[i][0], value: info.hashtags[i][1], checkable: true}, -1);
        var btn = hashFlow.getElement(idx);
        if(findInArray(info.hashtags[i][1], selectedElements) != -1){
            btn.clicked(info.hashtags[i][1]);
        }
        btn.clicked.connect(function(value){
                                for(var j=0; j< hashFlow.length(); j++ ){
                                    var x = hashFlow.getElement(j);
                                    if(x.checked){
                                        if(findInArray(x.value, selectedElements) == -1)
                                            selectedElements.push(x.value);
                                    }else{
                                        var found = findInArray(x.value, selectedElements);
                                        if(found != -1)
                                            selectedElements.splice(found, 1);
                                    }
                                }
                                root.hashClicked(selectedElements);
                                if(selectedElements.length == 0)
                                    showAllDots();
                            });
    }
    infoBaloon.addElement("ToolText.qml", "lt", {text: "Links utilizzati", "font.bold": true}, -1);
    var linkIdx = infoBaloon.addElement("ResultFlow.qml", "hash", {}, -1);
    var linkFlow = infoBaloon.getElement(linkIdx);
    for(var i in info.links){
        var index = linkFlow.addElement("ToolButton.qml", "l"+i, {text: info.links[i][1], value: info.links[i][1]}, -1);
        var btn = linkFlow.getElement(index);
        btn.clicked.connect(function(value){ root.linkClicked(value); });
    }
}
