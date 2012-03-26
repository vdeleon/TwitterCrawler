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

function emptyMap(){
    for(var i=locations.length-1; i>=0; i--){
        map.removeMapObject(locations[i]);
    }
    selectedRegion.topLeft.latitude = 0;
    selectedRegion.topLeft.longitude = 0;
    selectedRegion.bottomRight.latitude = 0;
    selectedRegion.bottomRight.longitude = 0;
}

function getPointInfo(index){
    toolBaloon.empty();
    toolBaloon.addElement("ToolText.qml", "element", {text: "Elementi in questo punto: "}, -1);
    newSearchIndex = toolBaloon.addElement("ToolButton.qml", "newSearch", {text: "Nuova Ricerca"}, -1);
    setNewSearchButton();
}
