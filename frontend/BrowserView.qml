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
import QtWebKit 1.0

View{
    id: root
    signal back()
    property string url: ""
    Flickable{
        id: flick
        anchors.fill: parent
        width: parent.width
        contentWidth: root.width
        contentHeight: web.height
        WebView{
            id: web
            url: root.url
            width: flick.width
        }
    }
    ToolBaloon{
        id: tools
        anchors.top: root.top
        anchors.left: root.left
        anchors.margins: 5
    }
    Component.onCompleted: {
        var i = tools.addElement("ToolButton.qml", "back", {text: "Indietro"}, -1);
        var el = tools.getElement(i);
        el.clicked.connect(function(){root.back();})
    }
}
