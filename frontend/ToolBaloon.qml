// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

import "ToolBaloon.js" as Tools

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
        opacity: 0.5
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
