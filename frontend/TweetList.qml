// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Item{
    id: root
    width: parent.width
    anchors.left: parent.left
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    anchors.leftMargin: width*-1
    anchors.topMargin: 5
    anchors.bottomMargin: 5
    Rectangle{
        anchors.fill: parent
        color: "#000"
        opacity: 0.8
        radius: 5
    }
    ListModel{
        id: model
    }
    ListView{
        id: view
        anchors.fill: parent
        anchors.margins: 5
        spacing: 4
        model: model
        clip: true
        delegate: Item{
            width: parent.width
            height: col.height
            Rectangle{
                anchors.fill: parent
                color: "#000"
                opacity: 0.4
            }
            Column{
                id: col
                width: parent.width-4
                anchors.margins: 2
                Text{
                    text: year+"/"+month+"/"+day+" "+hour+":"+minute
                    color: "white"
                    anchors.right: parent.right
                }
                Text{
                    text: "<a href=\"https://twitter.com/"+userName+"\">"+userName+"</a>"
                    onLinkActivated: Qt.openUrlExternally(link)
                    color: "white"
                    font.bold: true
                }
                Text{
                    text: tweet
                    wrapMode: Text.WordWrap
                    color: "white"
                    width: parent.width
                }
                Item{
                    height: 20
                }
                ToolButton{
                    checkable: true
                    visible: shower.checked
                    width: parent.width+4
                    text: qsTr("Draw user Track")
                    onCheckedChanged: {
                        if(checked){
                            rootPage.getUserTweets(userName);
                        } else {
                            defaultView.deleteUserTrack(userName);
                        }
                    }
                    Component.onCompleted: {
                        if(!visible){
                            if(!checked && defaultView.isTracked(userName)){
                                shower.clicked("");
                                checked = true;
                            }
                        }
                    }
                }
                ToolButton{
                    visible: shower.checked
                    width: parent.width+4
                    text: qsTr("Get more Tweets")
                    onClicked: {
                        rootPage.startHistoricalUserSearch(userName)
                    }
                }
                ToolButton{
                    id: shower
                    width: parent.width+4
                    text: "V"
                    checkable: true
                    onClicked: rotation+=180
                }
            }
        }
    }

    states: [
        State {
            name: "displayed"
            when: (model.count > 0)
            PropertyChanges {
                target: root
                anchors.leftMargin: 5
            }
        }
    ]

    transitions: [
        Transition {
            from: ""
            to: "displayed"
            reversible: true
            NumberAnimation{property: "anchors.leftMargin"; duration: 500; easing.type: Easing.InOutQuad}
        }
    ]

    function addItem(item){
        model.append(item);
    }

    function clear(){
        model.clear();
    }

}
