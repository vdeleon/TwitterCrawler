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
import QtMobility.location 1.2

MapImage{
    id: root
    property double latitude
    property double longitude
    property int dbId
    source: "images/map-dot.png"
    coordinate: Coordinate {
        latitude: root.latitude
        longitude: root.longitude
    }
    SequentialAnimation{
        id: appear
        loops: 1
        PropertyAnimation{
            target: root
            properties: "scale"
            from: 0
            to: 1.5
            duration: 300
        }
        PropertyAnimation{
            target: root
            properties: "scale"
            from: 1.5
            to: 1
            duration: 300
        }
    }
    Component.onCompleted: {
        appear.running = true
    }
}
