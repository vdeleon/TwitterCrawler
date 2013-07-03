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

Flow {
    id: root
    width: parent.width
    spacing: 2
    function addElement(object, name, customizations, group){
        var component = Qt.createComponent(object);
        var obj = component.createObject(root, customizations);
        if (obj == null) {
            console.log("Error creating object");
            return;
        }
        if(group == -1)
            return Tools.addElement(obj);
        return Tools.addToGroup(group, obj);
    }
    function getElement(index, group){
        return Tools.elements[index];
    }
    function empty(){
        Tools.empty();
    }
    function length(){
        return Tools.elements.length;
    }
}
