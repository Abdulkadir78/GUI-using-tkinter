import sqlite3


class Database:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.mycursor = self.connection.cursor()
        query = 'CREATE TABLE IF NOT EXISTS dishes (id INTEGER PRIMARY KEY, dish VARCHAR(150), price VARCHAR(50))'
        self.mycursor.execute(query)
        self.connection.commit()

# ------------Menu Functions-----------------------
    def fetch(self):
        self.mycursor.execute('SELECT dish, price FROM dishes')
        rows = self.mycursor.fetchall()
        return rows

    def insert(self, dish_name, dish_price):
        self.mycursor.execute(
            'INSERT INTO dishes VALUES (NULL, ?, ?)', (dish_name, dish_price))
        self.connection.commit()

    def remove(self, dish_name):
        self.mycursor.execute(
            'DELETE FROM dishes WHERE dish = ?', (dish_name,))
        self.connection.commit()

    def update(self, old_dish_name, new_dish_name, new_price):
        self.mycursor.execute('UPDATE dishes SET dish = ?, price = ? WHERE dish = ?',
                              (new_dish_name, new_price, old_dish_name))

        self.connection.commit()
# -------------------------------------------------

# ------------Bill Functions-----------------------
    def create_bill(self):
        query = 'CREATE TABLE IF NOT EXISTS bill (id INTEGER PRIMARY KEY, dish VARCHAR(150), price VARCHAR(50))'
        self.mycursor.execute(query)
        self.connection.commit()

    def drop_bill(self):
        self.mycursor.execute('DROP TABLE bill')
        self.connection.commit()

    def fetch_bill(self):
        self.mycursor.execute('SELECT * FROM bill')
        rows = self.mycursor.fetchall()
        return rows

    def insert_bill(self, dish_name, dish_price):
        self.mycursor.execute(
            'INSERT INTO bill VALUES (NULL, ?, ?)', (dish_name, dish_price))
        self.connection.commit()

    def remove_bill(self, dish_id):
        self.mycursor.execute(
            'DELETE FROM bill WHERE id = ?', (dish_id,))
        self.connection.commit()
# -------------------------------------------------

    def __del__(self):
        self.connection.close()
