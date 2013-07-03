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

import QtQuick 1.1
import QtWebKit 1.0

View{
    id: authDialog
    property string url: "about://blank"
    signal codeRecived(string auth)
    WebView{
        id: webView
        anchors.fill: parent
        //preferredHeight: parent.height
        url: authDialog.url
    }
    ToolBaloon{
        id: tools
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 5
        anchors.topMargin: 5
        Component.onCompleted: {
            tools.addElement("ToolText.qml", "title", {text: qsTr("Insert PIN here")}, -1);
            var code = tools.getElement(tools.addElement("ToolInput.qml", "input", {}, -1));
            var btn = tools.getElement(tools.addElement("ToolButton.qml", "btn", {text: qsTr("Access")}, -1));
            btn.clicked.connect(function(){
                                    authDialog.codeRecived(code.text);
                                });
        }
    }
}
