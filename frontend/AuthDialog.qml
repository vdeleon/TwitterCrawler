// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1
import QtWebKit 1.0

View{
    Column{
        anchors.fill: parent
        spacing: 20
        WebView{
            height: 400
            width: parent.width
            url: "http://www.google.it"
        }
        Rectangle{
            color: "#000"
            height: 100
            width: parent.width
        }
    }
}
