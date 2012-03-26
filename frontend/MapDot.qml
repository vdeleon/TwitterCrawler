// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1
import QtMobility.location 1.2

MapImage{
    id: root
    property double latitude
    property double longitude
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
