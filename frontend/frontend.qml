// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

PageStack{
    id: root
    width: 900
    height: 600
    currentPage: defaultView

    MainView{
        id: defaultView
    }

    AuthDialog{
        id: authDialog
        url: controller.loginUrl
        onCodeRecived: {
            controller.loginWithCode(auth)
        }
    }

    Component.onCompleted: {
        if(!controller.loggedIn){
            root.push(authDialog);
        }
    }
}
