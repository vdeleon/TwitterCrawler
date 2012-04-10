// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1
import QtWebKit 1.0

View{
    id: root
    signal back()
    property string url: ""
    Flickable{
        id: flick
        anchors.fill: parent
        width: parent.width
        contentWidth: root.width
        contentHeight: web.height
        WebView{
            id: web
            url: root.url
            width: flick.width
        }
    }
    ToolBaloon{
        id: tools
        anchors.top: root.top
        anchors.left: root.left
        anchors.margins: 5
    }
    Component.onCompleted: {
        var i = tools.addElement("ToolButton.qml", "back", {text: "Indietro"}, -1);
        var el = tools.getElement(i);
        el.clicked.connect(function(){root.back();})
    }
}
