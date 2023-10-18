class DatabaseUtil:
    def __init__(self):
        import sqlite3
        self.conn = sqlite3.connect('res/apple-spyder.db')

    def db_select(self, sql):
        try:
            c = self.conn.execute(sql)
            return c.fetchall()
        except ValueError as err:
            print(err)

    def db_operate(self, *sql):
        try:
            self.conn.execute(*sql)
            self.conn.commit()
        except ValueError as err:
            print(err)

    def close(self):
        self.conn.close()
