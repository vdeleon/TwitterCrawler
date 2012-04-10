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
