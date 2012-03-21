// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

PageStack{
    id: root
    width: 900
    height: 600
    currentPage: defaultView

    MainView{
        id: defaultView
        search: controller.search
        step: controller.step
        onNewSearch: {
            controller.createNewSearch();
        }
        onStartMapSearch: {
            controller.startMapSearch(lat1, long1, lat2, long2);
        }
    }

    AuthDialog{
        id: authDialog
        url: controller.loginUrl
        onCodeRecived: {
            controller.loginWithCode(auth)
            root.pop();
        }
    }

    Component.onCompleted: {
        root.push(defaultView)
        if(!controller.loggedIn){
            root.push(authDialog);
        }
    }
}
