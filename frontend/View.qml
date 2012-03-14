import QtQuick 1.1

Rectangle{
    width: parent.width
    height: parent.height
    color: "#fff"
    visible: false;
    onVisibleChanged: {
        if(visible == true){
            focus = true;
            return;
        }
        focus = false;
    }
}
