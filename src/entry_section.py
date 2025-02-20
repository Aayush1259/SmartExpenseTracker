import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from export import Export
from ml import categorize_expense, fraud_detection
import pandas as pd

# Define color and font constants
TEXT_COLOR = "#333333"      # Dark gray text
PRIMARY_COLOR = "#32CD32"   # Green for highlights
ACCENT_COLOR = "#FF6F61"    # Accent (buttons, borders)

class ExpenseEntryFrame(ttk.Frame):
    def __init__(self, parent, db, *args, **kwargs):
        super().__init__(parent, padding="20", *args, **kwargs)
        self.db = db
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title = ttk.Label(self, text="Add Expense", font=("Segoe UI", 16, "bold"), foreground=PRIMARY_COLOR)
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Expense Entry Form
        labels = ["Date:", "Expense Type:", "Amount:", "Description:"]
        for idx, text in enumerate(labels, start=1):
            ttk.Label(self, text=text, foreground=TEXT_COLOR).grid(row=idx, column=0, sticky="e", padx=5, pady=5)

        self.date_var = tk.StringVar()
        self.date_entry = DateEntry(self, textvariable=self.date_var, width=25,
                                    background="white", foreground="#000000", date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.category_combo = ttk.Combobox(self, width=23)
        self.category_combo["values"] = ["Food", "Transport", "Housing", "Utilities",
                                        "Entertainment", "Healthcare", "Education", "Shopping", "Insurance", "Other"]
        self.category_combo.grid(row=2, column=1, padx=5, pady=5)

        self.amount_entry = ttk.Entry(self, width=25, foreground="#000000")
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)

        self.description_entry = ttk.Entry(self, width=25, foreground="#000000")
        self.description_entry.grid(row=4, column=1, padx=5, pady=5)

        # Action Buttons
        ttk.Button(self, text="Add Expense", command=self.add_expense).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Export Data", command=self.export_data).grid(row=6, column=0, columnspan=2, pady=5)
        ttk.Button(self, text="View Expenses", command=self.view_expenses).grid(row=7, column=0, columnspan=2, pady=10)

        # Delete Expense Section
        ttk.Label(self, text="Expense ID to Delete:", foreground=TEXT_COLOR).grid(row=8, column=0, sticky="e", padx=5, pady=5)
        self.delete_id_entry = ttk.Entry(self, width=25, foreground="#000000")
        self.delete_id_entry.grid(row=8, column=1, padx=5, pady=5)
        ttk.Button(self, text="Delete Expense", command=self.delete_expense).grid(row=9, column=0, columnspan=2, pady=10)

        # Update Expense Section
        ttk.Label(self, text="Expense ID to Update:", foreground=TEXT_COLOR).grid(row=10, column=0, sticky="e", padx=5, pady=5)
        self.update_id_entry = ttk.Entry(self, width=25, foreground="#000000")
        self.update_id_entry.grid(row=10, column=1, padx=5, pady=5)
        ttk.Button(self, text="Update Expense", command=self.update_expense).grid(row=11, column=0, columnspan=2, pady=10)

        # Exit Button
        ttk.Button(self, text="Exit", command=self.exit_app).grid(row=12, column=0, columnspan=2, pady=(20, 5))

    def add_expense(self):
        date_val = self.date_var.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return
        desc = self.description_entry.get()
        category = self.category_combo.get().strip()
        if not category:
            category = categorize_expense(desc)
            self.category_combo.set(category)
        if self.db.insert_expense(date_val, amount, category, desc):
            messagebox.showinfo("Success", "Expense added successfully!")
            self.clear_fields()
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
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")]
        )
        if not file_path:
            return
        from export import Export
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

    def view_expenses(self):
        data = self.db.get_expenses()
        if not data:
            messagebox.showinfo("View Expenses", "No expense data available.")
            return
        view_window = tk.Toplevel(self)
        view_window.title("View Expenses")
        tree = ttk.Treeview(view_window, columns=("ID", "Date", "Amount", "Category", "Description"), show="headings")
        for col in ("ID", "Date", "Amount", "Category", "Description"):
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for row in data:
            tree.insert("", tk.END, values=row)
        tree.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def delete_expense(self):
        expense_id = self.delete_id_entry.get().strip()
        if not expense_id:
            messagebox.showerror("Error", "Please enter a valid Expense ID.")
            return
        try:
            expense_id = int(expense_id)
        except ValueError:
            messagebox.showerror("Error", "Expense ID must be an integer.")
            return
        if self.db.delete_expense(expense_id):
            messagebox.showinfo("Success", f"Expense with ID {expense_id} deleted successfully!")
            self.delete_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Failed to delete Expense ID {expense_id}.")

    def update_expense(self):
        update_id = self.update_id_entry.get().strip()
        if not update_id:
            messagebox.showerror("Error", "Please enter a valid Expense ID to update.")
            return
        try:
            update_id = int(update_id)
        except ValueError:
            messagebox.showerror("Error", "Expense ID must be an integer.")
            return
        date_val = self.date_var.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return
        desc = self.description_entry.get()
        category = self.category_combo.get().strip()
        if not category:
            category = categorize_expense(desc)
            self.category_combo.set(category)
        if self.db.update_expense(update_id, date_val, amount, category, desc):
            messagebox.showinfo("Success", f"Expense with ID {update_id} updated successfully!")
            self.update_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Failed to update Expense ID {update_id}.")

    def exit_app(self):
        self.winfo_toplevel().destroy()
