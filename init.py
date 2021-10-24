import os

from converter import UPLOAD_PATH
from converter import db


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_PATH):
        os.mkdir(UPLOAD_PATH)

    with db.db() as connection:
        connection.execute("create table if not exists documents"
                           " (id integer primary key autoincrement, "
                           "uuid text, pages integer, ready integer, "
                           "status text, msg text, filename text);")
        connection.execute("create table if not exists nlp"
                           " (id integer primary key autoincrement, "
                           "uuid text, page integer, status text, json text, final text);")
        connection.execute("create table if not exists include"
                           " (id integer primary key autoincrement, word text unique on conflict ignore);")
        connection.execute("create table if not exists exclude"
                           " (id integer primary key autoincrement, word text unique on conflict ignore);")
