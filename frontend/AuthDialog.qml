import QtQuick 1.1
import QtWebKit 1.0
import QtDesktop 0.1

View{
    id: authDialog
    property string url: "about://blank"
    signal codeRecived(string auth)
    ScrollArea{
        id: webFlick
        width: parent.width
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.left: parent.left
        anchors.bottom: btns.top
        contentHeight: webView.height
        clip: true
        WebView{
            id: webView
            width: webFlick.width-15
            //preferredHeight: parent.height
            url: authDialog.url
        }
    }
    Rectangle{
        id: btns
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.left: parent.left
        height: 100
        Row{
            anchors.centerIn: parent
            Label{
                height: authCode.height
                verticalAlignment: Text.AlignVCenter
                font.pointSize: 12
                text: qsTr("Insert PIN here: ")
            }
            TextField{
                id: authCode
            }
        }
        Button{
            id: authButton
            anchors.bottom: parent.bottom
            anchors.left: parent.right
            anchors.bottomMargin: 10
            anchors.leftMargin: -10-authButton.width
            text: qsTr("Accept")
            onClicked: {
                authDialog.codeRecived(authCode.text);
            }
        }
    }
}
