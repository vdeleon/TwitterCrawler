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

import "ContentManagement.js" as Tools

Item {
    id: root
    width: 250
    height: column.height+7
    function addElement(object, name, customizations, group){
        var component = Qt.createComponent(object);
        var obj = component.createObject(column, customizations);
        if (obj == null) {
            console.log("Error creating object");
            return;
        }
        if(group == -1)
            return Tools.addElement(obj);
        return Tools.addToGroup(group, obj);
    }
    function addGroup(){
        return Tools.addGroup();
    }
    function deleteGroup(index){
        Tools.deleteGroup(index);
    }
    function getElement(index, group){
        return Tools.elements[index];
    }
    function empty(){
        Tools.empty();
    }
    Rectangle{
        anchors.fill: parent
        color: "#000"
        opacity: 0.8
        radius: 5
    }
    Column{
        id: column
        anchors.top: root.top
        anchors.right: root.right
        anchors.left: root.left
        anchors.margins: 3
        spacing: 1
        add: Transition{
            NumberAnimation {properties: "opacity"; from: 0; to: 1; duration: 500; /*easing.type: Easing.OutQuad */}
        }
        move: Transition {
            NumberAnimation {
                properties: "y"
                easing.type: Easing.OutQuad
                duration: 500
            }
        }
    }

    Behavior on height {NumberAnimation{duration: 500; easing.type: Easing.OutQuad}}
}
