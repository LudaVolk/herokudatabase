import sqlite3


class DBHelper:

    def __init__(self, dbname="database_vl.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def setup(self):
        stmt = "SELECT * FROM test"
        self.conn.execute(stmt)
        self.conn.commit()

    def check_user_id(self, user_id):
        stmt = "SELECT COUNT(*) FROM test  WHERE user_id = ?"
        args = (user_id, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    def db_table_val(self, user_id, user_name, user_surname, username):

        stmt = "INSERT INTO test (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)"
        args = (user_id, user_name, user_surname, username)
        print(args)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def db_table_name(self, id, name, surname, phone,  classes):
        stmt = "INSERT INTO Users_test (id, name, surname, phone, classes) VALUES (?, ?, ?, ?, ?)"
        args = (id, name, surname, phone, classes)
        print(args)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def user_save(self, name, surname, phone, classes):
        stmt = "UPDATE Users_test SET name = ? WHERE surname = ? AND phone = ? AND classes = ?"
        args = (name, surname, phone, classes)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def user_add(self, name, surname, phone, classes):
        stmt = "INSERT INTO Users_test (name, surname, phone, classes) VALUES (?, ?, ?, ?)"
        args = (name, surname, phone, classes)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT classes, name, phone FROM Users_test"
        #args = (classes,)
        return [x for x in self.conn.execute(stmt,)]

    def get_all_classes(self, classes):
         stmt = "SELECT classes, name, surname, phone FROM Users_test WHERE classes = ?"
         args = (classes,)
         return [x for x in self.conn.execute(stmt, args)]

    def get_classes_inf(self, classes):
        stmt = "SELECT * FROM Users_test WHERE classes = ?"
        args = (classes,)
        self.conn.execute(stmt, args)
        curr = self.conn.cursor()
        data = curr.fetchall()
        return data

