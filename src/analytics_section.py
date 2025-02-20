import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import seaborn as sns
from ml import (
    forecast_expenses, personalized_budget_recommendation,
    smart_expense_insights, spending_categories, balance_trend
)

TEXT_COLOR = "#000000"
PRIMARY_COLOR = "#32CD32"
ACCENT_RED = "#FF0000"
ACCENT_YELLOW = "#FFFF00"
ACCENT_BLUE = "#0000FF"
GRAY_COLOR = "#A8A8A8"
BACKGROUND_COLOR = "#FFFFFF"

class AnalyticsFrame(ttk.Frame):
    def __init__(self, parent, db, *args, **kwargs):
        super().__init__(parent, padding="10", *args, **kwargs)
        self.db = db
        self.create_widgets()

    def create_widgets(self):
        self.summary_label = ttk.Label(self, text="", font=("Segoe UI", 12, "italic"), foreground=PRIMARY_COLOR)
        self.summary_label.pack(pady=(0, 10))

        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(filter_frame, text="From:", foreground=TEXT_COLOR).pack(side=tk.LEFT, padx=5)
        self.start_date = DateEntry(filter_frame, width=12, background="white", foreground="#000000", date_pattern="yyyy-mm-dd")
        self.start_date.pack(side=tk.LEFT, padx=5)
        ttk.Label(filter_frame, text="To:", foreground=TEXT_COLOR).pack(side=tk.LEFT, padx=5)
        self.end_date = DateEntry(filter_frame, width=12, background="white", foreground="#000000", date_pattern="yyyy-mm-dd")
        self.end_date.pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Apply Filters", command=self.show_analysis).pack(side=tk.RIGHT, padx=5)

        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(control_frame, text="Analysis Type:", foreground=TEXT_COLOR).pack(side=tk.LEFT, padx=5)
        self.analysis_type = tk.StringVar(value="Monthly")
        for opt in ["Weekly", "Monthly", "Yearly"]:
            ttk.Radiobutton(control_frame, text=opt, variable=self.analysis_type, value=opt).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Show Analysis", command=self.show_analysis).pack(side=tk.RIGHT, padx=5)

        ai_frame = ttk.Frame(self)
        ai_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(ai_frame, text="Forecast Expenses", command=self.show_forecast).pack(side=tk.LEFT, padx=5)
        ttk.Button(ai_frame, text="Budget Recommendation", command=self.show_budget_recommendation).pack(side=tk.LEFT, padx=5)
        ttk.Button(ai_frame, text="Spending Categories", command=self.show_spending_categories).pack(side=tk.LEFT, padx=5)
        ttk.Button(ai_frame, text="Balance Trend", command=self.show_balance_trend).pack(side=tk.LEFT, padx=5)

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.update_summary()

    def update_summary(self):
        data = pd.DataFrame(self.db.get_expenses(), columns=["id", "date", "amount", "category", "description"])
        self.summary_label.config(text=f"Expense Insights: {smart_expense_insights(data)}")

    def show_analysis(self):
        data = pd.DataFrame(self.db.get_expenses(), columns=["id", "date", "amount", "category", "description"])
        if data.empty:
            messagebox.showinfo("No Data", "No expense data available.")
            return
        data["date"] = pd.to_datetime(data["date"])
        start = pd.to_datetime(self.start_date.get_date())
        end = pd.to_datetime(self.end_date.get_date())
        data = data[(data["date"] >= start) & (data["date"] <= end)]
        if data.empty:
            messagebox.showinfo("No Data", "No expense data in this range.")
            return
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
        sns.set_style("whitegrid")
        sns.set_palette([ACCENT_RED, ACCENT_YELLOW, ACCENT_BLUE])
        data.set_index("date", inplace=True)
        if self.analysis_type.get() == "Weekly":
            df_resampled = data.resample("W-Mon").sum()
            self.plot_barchart(ax1, df_resampled, "Weekly")
        elif self.analysis_type.get() == "Monthly":
            df_resampled = data.resample("M").sum()
            self.plot_barchart(ax1, df_resampled, "Monthly")
        else:
            df_resampled = data.resample("Y").sum()
            self.plot_barchart(ax1, df_resampled, "Yearly")
        self.plot_pie_chart(ax2, data.reset_index())
        fig.tight_layout(pad=1.0)
        self.plot_canvas(fig)

    def plot_barchart(self, ax, df, label):
        if df.empty:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", color=PRIMARY_COLOR, fontsize=10)
            return
        bars = ax.bar(df.index, df["amount"], color=PRIMARY_COLOR)
        ax.set_title(f"{label} Analysis", color=PRIMARY_COLOR, fontsize=10)
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f'${h:,.0f}', xy=(bar.get_x() + bar.get_width()/2, h),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', color="#000000", fontsize=9)
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True, color=GRAY_COLOR, linestyle="--", linewidth=0.5, alpha=0.7)
        ax.set_axisbelow(True)

    def plot_pie_chart(self, ax, data):
        cat_totals = data.groupby("category")["amount"].sum()
        if cat_totals.empty:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", color=PRIMARY_COLOR, fontsize=10)
        else:
            slice_colors = [ACCENT_RED, ACCENT_YELLOW, ACCENT_BLUE]
            explode = [0.1] + [0]*(len(cat_totals)-1)
            ax.pie(cat_totals, labels=cat_totals.index, autopct='%1.1f%%', startangle=90,
                colors=slice_colors*(len(cat_totals)//len(slice_colors)+1),
                explode=explode, textprops={'color':"#000000", 'fontsize':9})
            ax.set_title("Expense Distribution", color=PRIMARY_COLOR, fontsize=10)

    def show_forecast(self):
        data = self._get_data()
        if data.empty:
            return
        from ml import forecast_expenses
        fdf = forecast_expenses(data, periods=1)
        if fdf.empty:
            messagebox.showinfo("Forecast", "Unable to forecast.")
            return
        self._clear_charts()
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(fdf["date"], fdf["forecast"], marker='o', color=ACCENT_RED)
        ax.set_title("Next Month Forecast", color=ACCENT_RED, fontsize=12)
        ax.grid(True, linestyle="--", alpha=0.7)
        fig.tight_layout()
        self.plot_canvas(fig)

    def show_budget_recommendation(self):
        data = self._get_data()
        if data.empty:
            return
        from ml import personalized_budget_recommendation
        rec = personalized_budget_recommendation(data)
        if rec:
            messagebox.showinfo("Budget Recommendation", f"Suggested monthly budget: ${rec:,.2f}")
        else:
            messagebox.showinfo("Budget Recommendation", "Not enough data.")

    def show_spending_categories(self):
        data = self._get_data()
        if data.empty:
            return
        from ml import spending_categories
        cats = spending_categories(data)
        self._clear_charts()
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(cats.keys(), cats.values(), color=[ACCENT_RED, ACCENT_YELLOW, ACCENT_BLUE])
        ax.set_title("Must / Need / Want", color=PRIMARY_COLOR, fontsize=12)
        ax.grid(True, linestyle="--", alpha=0.7)
        fig.tight_layout()
        self.plot_canvas(fig)

    def show_balance_trend(self):
        data = self._get_data()
        if data.empty:
            return
        from ml import balance_trend
        trend = balance_trend(data)
        self._clear_charts()
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(trend["date"], trend["cumulative"], marker='o', color=ACCENT_BLUE)
        ax.set_title("Balance Trend", color=ACCENT_BLUE, fontsize=12)
        ax.grid(True, linestyle="--", alpha=0.7)
        fig.tight_layout()
        self.plot_canvas(fig)

    def _get_data(self):
        data = pd.DataFrame(self.db.get_expenses(), columns=["id", "date", "amount", "category", "description"])
        if data.empty:
            messagebox.showinfo("No Data", "No expense data.")
        else:
            data["date"] = pd.to_datetime(data["date"])
        return data

    def _clear_charts(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

    def plot_canvas(self, figure):
        canvas = FigureCanvasTkAgg(figure, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        import matplotlib.pyplot as plt
        plt.close(figure)
