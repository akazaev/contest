import sqlite3

from converter import DB


def get_connection():
    connection = sqlite3.connect(DB)
    return connection
