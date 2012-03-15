// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Item{
    id: stackedView
    width: 900
    height: 550
    signal ready();

    function push(view){
        stackedView.children.push(view);
        for(v in stackedView.children)
            if(stackedView.children[v].visible == true){
                stackedView.children[v].visible = false;
            }
        view.visible = true;
    }

    function addAndPush(source, name){
        var component = Qt.createComponent(source);
        if(component.status == Component.Error){
            console.log("Error creating component", component.errorString());
            return;
        }
        var object = component.createObject(stackedView);
        object.objectName = name;
        for(v in stackedView.children)
            if(stackedView.children[v].visible == true){
                stackedView.children[v].visible = false;
            }
        object.visible = true;
        return object;
    }

    //TODO: add a bottom bar or a top bar that can be populated with back button
}
