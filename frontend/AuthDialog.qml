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
        height: 400
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.left: parent.left
        contentHeight: webView.height
        clip: true
        WebView{
            id: webView
            preferredWidth: parent.width
            preferredHeight: 400
            url: authDialog.url
        }
    }
    Rectangle{
        anchors.top: webFlick.bottom
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.left: parent.left
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
