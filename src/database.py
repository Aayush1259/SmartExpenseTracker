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
        except Exception as e:
            print("Insert expense error:", e)
            return False

    def get_expenses(self):
        try:
            self.cursor.execute("SELECT * FROM expenses")
            return self.cursor.fetchall()
        except Exception as e:
            print("Get expenses error:", e)
            return []

    def delete_expense(self, expense_id):
        try:
            self.cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print("Delete expense error:", e)
            return False

    def update_expense(self, expense_id, date, amount, category, description):
        try:
            self.cursor.execute(
                "UPDATE expenses SET date = ?, amount = ?, category = ?, description = ? WHERE id = ?",
                (date, amount, category, description, expense_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print("Update expense error:", e)
            return False

    def __del__(self):
        if self.conn:
            self.conn.close()
