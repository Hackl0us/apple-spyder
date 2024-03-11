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

    def find_and_update_os_ota_record(self, os_name, published_date):
        try:
            c = self.conn.execute("SELECT * FROM os_ota_update WHERE os_name=?", (os_name,))
            if c.fetchall():
                return False
            else:
                self.conn.execute("INSERT INTO os_ota_update (os_name, update_time) VALUES (?, ?)", (os_name, published_date))
                self.conn.commit()
                return True
        except ValueError as err:
            print(err)

    def close(self):
        self.conn.close()
