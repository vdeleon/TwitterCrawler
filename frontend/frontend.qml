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
import QtMobility.location 1.2
import "tweets.js" as Tweets

PageStack{
    id: rootPage
    width: 900
    height: 600
    currentPage: defaultView

    function getUserTweets(userName){
        controller.getUserTweets(userName)
    }

    function startHistoricalUserSearch(userName){
        controller.startHistoricalUserSearch(userName)
    }

    Controller{
        id: controller
        onTweetsUpdated: {
            var tw = tweets
            for(var i in tw){
                var id = Tweets.addTweet(tw[i]);
                defaultView.addTweet(id);
            }
        }

        Component.onCompleted: {
            userTracked.connect(function(ids){
                                    var userId = Tweets.getTweetById(ids[0]).userName
                                    var object = defaultView.addTrackToMap(userId);
                                    for(var i in ids){
                                        var tweet = Tweets.getTweetById(ids[i]);
                                        if(tweet.location != false){
                                            var coordinate = Qt.createQmlObject("import QtQuick 1.1; import QtMobility.location 1.2;"
                                                                            +"Coordinate{ latitude: "+ tweet.location.lat+";"
                                                                            +"longitude: "+tweet.location.lon+"; }", object, "coord");
                                            object.addCoordinate(coordinate);
                                        }
                                    }
                                    defaultView.refreshAllPoints();
                                });
        }
    }

    MainView{
        id: defaultView

        onStartHistoricalMapSearch: {
            controller.startHistoricalMapSearch(lat1, long1, lat2, long2, delta)
        }

        onStartHistoricalContentSearch: {
            controller.startHistoricalContentSearch(content, delta)
        }

        onStartRealtimeMapSearch: {
            controller.startRealtimeMapSearch(lat1, long1, lat2, long2)
        }

        onStartRealtimeContentSearch: {
            controller.startRealtimeContentSearch(content)
        }

        onStopSearch: {
            controller.stop()
        }

        onSaveSearch: {
            rootPage.push(saveView)
        }

        onLinkClicked: {
            browserView.url = url;
            rootPage.push(browserView);
        }
        onAddPage: {
            controller.getMoreHistoricalResults();
        }
    }

    AuthDialog{
        id: authDialog
        url: controller.loginUrl
        onCodeRecived: {
            controller.loginWithCode(auth)
            rootPage.pop();
        }
    }

    SaveView{
        id: saveView
    }

    Component.onCompleted: {
        rootPage.push(defaultView)
        if(!controller.loggedIn){
            rootPage.push(authDialog);
        }
    }
}
