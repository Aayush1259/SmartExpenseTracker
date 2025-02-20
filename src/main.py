import tkinter as tk
from tkinter import ttk
from database import Database
from entry_section import ExpenseEntryFrame
from analytics_section import AnalyticsFrame

def main():
    root = tk.Tk()
    root.title("Smart Expense Tracker")
    root.geometry("1200x700")

    # Set up a modern ttk style
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TFrame", background="#F7F7F7")
    style.configure("TLabel", background="#F7F7F7", foreground="#333333", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=5)
    style.configure("TEntry", font=("Segoe UI", 10))
    style.configure("TCombobox", font=("Segoe UI", 10))

    # Main frame
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Initialize database
    db = Database()

    # Left: Expense Entry (with add, delete, update, view, export, exit)
    entry_frame = ExpenseEntryFrame(main_frame, db)
    entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

    # Right: Analytics
    analytics_frame = AnalyticsFrame(main_frame, db)
    analytics_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
