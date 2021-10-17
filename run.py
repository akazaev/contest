import os
import sqlite3

from converter import UPLOAD_PATH, DB
from converter.web.app import create_app


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_PATH):
        os.mkdir(UPLOAD_PATH)

    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute("create table if not exists documents"
                   " (id integer primary key autoincrement, "
                   "uuid text, pages integer, ready integer, "
                   "status text, msg text, filename text);")
    connection.commit()

    app = create_app()
    app.run(debug=True)
