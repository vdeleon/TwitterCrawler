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

Item{
    id: root
    width: parent.width
    height: 30*2
    property int searchType: typeGroup.selectedValue
    signal searchContentChanged(int value)
    RadioGroup{
        id: typeGroup
        selectedValue: 2
    }
    RadioGroup{
        id: contentGroup
        onSelectedValueChanged: {
            root.searchContentChanged(selectedValue);
        }
        selectedValue: 2
    }

    Column{
        anchors.fill: parent
        Row{
            id: searchOptions
            width: parent.width
            RadioButton{
                width: root.width/2
                text: qsTr("Realtime")
                group: typeGroup
                value: 2
            }
            RadioButton{
                width: root.width/2
                text: qsTr("Historical")
                group: typeGroup
                value: 1
            }
        }
        Row{
            width: parent.width
            RadioButton{
                width: root.width/2
                text: qsTr("Map Zone")
                group: contentGroup
                value: 1
            }
            RadioButton{
                width: root.width/2
                text: qsTr("Content")
                group: contentGroup
                value: 2
            }
        }
        Component.onCompleted: {
            searchContentChanged(2)
        }
    }
}
