// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

StackedView{
    id: mainView
    children: []
    Component.onCompleted: {
        if(!controller.loggedIn){
            var obj = mainView.addAndPush("AuthDialog.qml", "authDialog");
            obj.url = controller.loginUrl;
        }
    }
}
