import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from ml import categorize_expense, fraud_detection
import pandas as pd

class ExpenseEntryFrame(ttk.Frame):
    """
    Left-side panel for adding expenses, exporting data, and an Exit button at the bottom.
    """
    def __init__(self, parent, db, *args, **kwargs):
        super().__init__(parent, padding="20", *args, **kwargs)
        self.db = db
        self.create_widgets()

    def create_widgets(self):
        # Title
        ttk.Label(self, text="Add Expense", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Date
        self.date_var = tk.StringVar()
        ttk.Label(self, text="Date:", foreground="#000000").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = DateEntry(self, textvariable=self.date_var, width=25,
                                    background="white", foreground="#000000",
                                    date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        # Category
        ttk.Label(self, text="Expense Type:", foreground="#000000").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.category_combo = ttk.Combobox(self, width=23)
        self.category_combo["values"] = [
            "Food", "Transport", "Housing", "Utilities", "Entertainment",
            "Healthcare", "Education", "Shopping", "Insurance", "Other"
        ]
        self.category_combo.grid(row=2, column=1, padx=5, pady=5)

        # Amount
        ttk.Label(self, text="Amount:", foreground="#000000").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.amount_entry = ttk.Entry(self, width=25, foreground="#000000")
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)

        # Description
        ttk.Label(self, text="Description:", foreground="#000000").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.description_entry = ttk.Entry(self, width=25, foreground="#000000")
        self.description_entry.grid(row=4, column=1, padx=5, pady=5)

        # Buttons: Add Expense, Export Data
        ttk.Button(self, text="Add Expense", command=self.add_expense).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Export Data", command=self.export_data).grid(row=6, column=0, columnspan=2, pady=5)

        # Exit button at the bottom
        ttk.Button(self, text="Exit", command=self.exit_app).grid(row=7, column=0, columnspan=2, pady=(20, 5))

    def add_expense(self):
        date_val = self.date_var.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return
        desc = self.description_entry.get()
        category = self.category_combo.get().strip()
        if not category:
            category = categorize_expense(desc)
            self.category_combo.set(category)

        if self.db.insert_expense(date_val, amount, category, desc):
            messagebox.showinfo("Success", "Expense added successfully!")
            self.clear_fields()

            # Fraud detection
            records = self.db.get_expenses()
            if records:
                df = pd.DataFrame(records, columns=["id", "date", "amount", "category", "description"])
                if fraud_detection(amount, df["amount"].dropna()):
                    messagebox.showwarning("Anomaly", "Unusually high expense detected!")
        else:
            messagebox.showerror("Error", "Failed to add expense.")

    def clear_fields(self):
        self.date_var.set("")
        self.amount_entry.delete(0, tk.END)
        self.category_combo.set("")
        self.description_entry.delete(0, tk.END)

    def export_data(self):
        from export import Export
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")]
        )
        if not file_path:
            return
        exporter = Export(self.db)
        success = False
        if file_path.endswith(".xlsx"):
            success = exporter.to_excel(file_path)
        elif file_path.endswith(".csv"):
            success = exporter.to_csv(file_path)
        if success:
            messagebox.showinfo("Export", "Data exported successfully!")
        else:
            messagebox.showerror("Error", "Export failed.")

    def exit_app(self):
        """
        Closes the entire application window.
        """
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.winfo_toplevel().destroy()
