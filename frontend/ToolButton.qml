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

Item {
    id: button
    signal clicked(string value)
    property string text: "ClickMe"
    property bool checkable: false
    property bool checked: false
    property string value: ""
    width: Math.max(244, (text.width+6))
    height: 30
    onClicked: {
        if(checkable){
            checked = !checked;
            if(checked)
                buttonColor.color = "#fff";
            else
                buttonColor.color = "#000";
        }
    }
    Rectangle{
        id: buttonColor
        color: "#000"
        opacity: 0.4
        anchors.fill: parent
        MouseArea{
            anchors.fill: parent
            onPressed: {
                buttonColor.color = "#fff"
            }
            onReleased: {
                buttonColor.color = "#000"
            }
            onClicked: {
                button.clicked(button.value);
            }
        }
    }
    Text{
        id: text
        anchors.centerIn: parent
        color: "#fff"
        text: button.text
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }
}
