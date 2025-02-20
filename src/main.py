import tkinter as tk
from tkinter import ttk
from database import Database
from entry_section import ExpenseEntryFrame
from analytics_section import AnalyticsFrame

def main():
    """
    Main entry point of the application with default system background (no gradient).
    """
    root = tk.Tk()
    root.title("Smart Expense Tracker")
    root.geometry("1200x700")

    # Create main frame (no gradient, no menubar, no bottom exit button).
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Initialize database
    db = Database()

    # Left: Expense Entry
    entry_frame = ExpenseEntryFrame(main_frame, db)
    entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

    # Right: Analytics
    analytics_frame = AnalyticsFrame(main_frame, db)
    analytics_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Run the application
    try:
        root.mainloop()
    except KeyboardInterrupt:
        # Typically triggered if the script is forcibly interrupted
        print("Application was interrupted (KeyboardInterrupt). Exiting gracefully.")

if __name__ == "__main__":
    main()
