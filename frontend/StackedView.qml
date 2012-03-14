// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Item{
    id: stackedView
    width: 900
    height: 550

    function push(view){
        stackedView.children.push(view);
        for(v in stackedView.children)
            if(stackedView.children[v].visible == true){
                stackedView.children[v].visible = false;
            }
         view.visible = true;
     }
    //TODO: add a bottom bar or a top bar that can be populated with back button
}
