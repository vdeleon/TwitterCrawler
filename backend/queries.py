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
table_searches = '''CREATE TABLE "searches" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "date" TEXT,
    "descr" TEXT,
    "total_steps" INTEGER NOT NULL DEFAULT (0)
)'''

table_users = '''CREATE TABLE "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "t_id" INTEGER NOT NULL,
    "t_screen_name" TEXT NOT NULL,
    "search" INTEGER NOT NULL REFERENCES searches(id) ON DELETE CASCADE,
    "step" INTEGER NOT NULL DEFAULT (1)
)'''

table_locations = '''CREATE TABLE "locations" (
    "user" INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    "date" TEXT,
    "lat" REAL NOT NULL,
    "long" REAL NOT NULL
)'''

table_followers = '''CREATE TABLE "followers" (
    "user" INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    "follower" INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
)'''

table_hashtags = '''CREATE TABLE "hashtags" (
    "user" INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    "tag" TEXT NOT NULL
)'''

table_links = '''CREATE TABLE "links" (
    "user" INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE, 
    "address" TEXT NOT NULL 
)'''

table_options = '''CREATE TABLE "options" (
    "key" TEXT,
    "value" TEXT
)'''

add_search_step = '''UPDATE "searches" 
SET "total_steps"=(SELECT "total_steps" FROM "searches" WHERE "id"=?)+1 
WHERE "id"=?'''