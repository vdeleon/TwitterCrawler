// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1
import TwitterCrawler 1.0

PageStack{
    id: root
    width: 900
    height: 600
    currentPage: defaultView

    Controller{
        id: controller
        onLocationsUpdated: {
            for(var i in locations)
                defaultView.addMapObject(locations[i].id,
                                         locations[i].username,
                                         locations[i].lat,
                                         locations[i].lon);
        }
        onPointInfoPrepared: {
            console.log(pointsInfo)
            defaultView.showPointInfo(pointsInfo)
        }
    }

    MainView{
        id: defaultView
        onNewSearch: {
            controller.createNewSearch();
        }
        onStartMapSearch: {
            controller.startMapSearch(lat1, long1, lat2, long2);
        }
        onStopSearch: {
            controller.stop()
        }
        onRequestPointInfo: {
            controller.getPointInfo(points);
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
