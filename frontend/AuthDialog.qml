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
import QtDesktop 0.1

View{
    id: authDialog
    property string url: "about://blank"
    signal codeRecived(string auth)
    ScrollArea{
        id: webFlick
        width: parent.width
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.left: parent.left
        anchors.bottom: btns.top
        contentHeight: webView.height
        clip: true
        WebView{
            id: webView
            width: webFlick.width-15
            //preferredHeight: parent.height
            url: authDialog.url
        }
    }
    Rectangle{
        id: btns
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.left: parent.left
        height: 100
        Row{
            anchors.centerIn: parent
            Label{
                height: authCode.height
                verticalAlignment: Text.AlignVCenter
                font.pointSize: 12
                text: qsTr("Insert PIN here: ")
            }
            TextField{
                id: authCode
            }
        }
        Button{
            id: authButton
            anchors.bottom: parent.bottom
            anchors.left: parent.right
            anchors.bottomMargin: 10
            anchors.leftMargin: -10-authButton.width
            text: qsTr("Accept")
            onClicked: {
                authDialog.codeRecived(authCode.text);
            }
        }
    }
}
