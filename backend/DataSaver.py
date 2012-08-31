'''
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
    
'''
from PySide.QtCore import QObject, Signal

class DataSaver(QObject):
    
    resultsUpdated = Signal()
    
    def __init__(self, db):
        QObject.__init__(self)
        self.db = db
        
    def saveResults(self, step):
        search = self.db.getLastSearchId()
        step = self.db.getSteps()
        for u in step.users:
            self.db.addUser(u.id, u.name, self.search, step)
            for f in u.followers:
                self.db.addFollower(f.id, f.name, search, step, self.db.getUserId(t_screen_name=u.name))
        for t in step.tweets:
            print t.hashtags
            self.db.addUser(t.user.id, t.user.name, search, step)
            userId = self.db.getUserId(t.user.name)
            if t.location != None:
                self.db.addLocation(userId, t.time, t.location[0], t.location[1])
            for tag in t.hashtags:
                self.db.addHashtag(userId, tag)
            for link in t.links:
                self.db.addLink(userId, link)
        self.resultsUpdated.emit()
        