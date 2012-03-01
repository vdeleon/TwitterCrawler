table_creation = '''CREATE TABLE "searches" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "date" TEXT,
    "descr" TEXT,
    "total_steps" INTEGER NOT NULL DEFAULT (1)
);

CREATE TABLE "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "t_id" INTEGER NOT NULL,
    "t_screen_name" TEXT NOT NULL,
    "search" INTEGER NOT NULL,
    "step" INTEGER NOT NULL DEFAULT (1)
);

CREATE TABLE "locations" (
    "user" INTEGER NOT NULL,
    "date" TEXT,
    "lat" REAL NOT NULL,
    "long" REAL NOT NULL
);

CREATE TABLE "followers" (
    "user" INTEGER NOT NULL,
    "follower" INTEGER NOT NULL
);

CREATE TABLE "hashtags" (
    "user" INTEGER NOT NULL,
    "tag" TEXT NOT NULL
);

CREATE TABLE "links" (
    "user" INTEGER NOT NULL,
    "address" TEXT NOT NULL
);'''

delete_search = '''DELETE FROM searches s, users u, locations l, followers f, hashtags h, links l 
WHERE s.id=:id AND u.search=s.id AND l.user=u.id AND f.user=u.id AND h.user=u.id AND l.user=u.id'''