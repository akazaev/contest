from converter.db.sqlite import get_connection as sql_connection


def get_connection():
    return sql_connection()


class db:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = get_connection()
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
