/*
Copyright (C) 2012 Riccardo Ferrazzo <f.riccardo87@gmail.com>

This file is part of TwitterCrawler.

    TwitterCrawler is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TwitterCrawler is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with TwitterCrawler.  If not, see <http://www.gnu.org/licenses/>

*/
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
                                         locations[i].lat,
                                         locations[i].lon);
        }
        onPointInfoPrepared: {
            defaultView.showPointInfo(pointsInfo)
        }
        onSimilarHashtagsPrepared: {
            defaultView.showOnlyDots(hashtags)
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
        onStartContentSearch: {
            controller.startContentSearch(content)
        }

        onStopSearch: {
            controller.stop()
        }
        onRequestPointInfo: {
            controller.getPointInfo(points);
        }
        onLinkClicked: {
            browserView.url = url;
            root.push(browserView);
        }
        onHashClicked: {
            controller.getSimilarHashtags(hash);
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

    BrowserView{
        id: browserView
        onBack: {
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
