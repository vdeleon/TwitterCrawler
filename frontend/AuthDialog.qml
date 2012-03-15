// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1
import QtWebKit 1.0

View{
    id: authDialog
    property string url: "http://www.google.it"
    Flickable{
        id: webFlick
        width: parent.width
        height: 400
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.left: parent.left
        flickableDirection: Flickable.VerticalFlick
        contentHeight: webView.height
        clip: true
        WebView{
            id: webView
            preferredWidth: parent.width
            preferredHeight: 400
            url: authDialog.url
        }
    }
    ScrollBar {
        target: webFlick
    }
    Rectangle{
        color: "#000"
        anchors.top: webFlick.bottom
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.left: parent.left
    }
}
