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

delete_search = '''DELETE FROM searches WHERE id=:id'''

add_search_step = '''UPDATE "searches" 
SET "total_steps"=(SELECT "total_steps" FROM "searches" WHERE "id"=:ida)+1 
WHERE "id"=:idb'''