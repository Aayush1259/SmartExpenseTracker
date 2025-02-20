import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("expense_tracker.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                amount REAL,
                category TEXT,
                description TEXT
            )
        ''')
        self.conn.commit()

    def insert_expense(self, date, amount, category, description):
        try:
            self.cursor.execute(
                "INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)",
                (date, amount, category, description)
            )
            self.conn.commit()
            return True
        except:
            return False

    def get_expenses(self):
        self.cursor.execute("SELECT * FROM expenses")
        return self.cursor.fetchall()

    def __del__(self):
        if self.conn:
            self.conn.close()
