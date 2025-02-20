# SmartExpenseTracker
Mini Project of Expense Tracker

# Smart Expense Tracker

Smart Expense Tracker is a lightweight personal finance management application built using Python, Tkinter, and SQLite. The app allows users to record their expenses, export data, and view interactive visual analytics including weekly, monthly, and yearly breakdowns. It also integrates basic machine learning features such as auto-categorization, anomaly detection, expense forecasting, and budget recommendations.

## Features

- **Expense Entry:**  
  - Record expenses with date, amount, category, and description.
  - Auto-categorize expenses using a simple machine-learning model when no category is provided.

- **Data Export:**  
  - Export expense data to CSV or Excel files.

- **Interactive Analytics:**  
  - Visualize expenses with bar charts and pie charts.
  - Filter data by a user-defined "From" and "To" date range.
  - Choose between weekly, monthly, or yearly analysis.

- **Forecasting & Budgeting:**  
  - Forecast future expenses using linear regression.
  - Receive personalized budget recommendations based on historical spending.

- **Anomaly Detection:**  
  - Detect unusually high expenses by comparing new entries against historical data using statistical thresholds and the IsolationForest algorithm.

- **Additional Insights:**  
  - Categorize spending into "Must," "Need," and "Want."
  - Display cumulative expense trends (balance trend).

## Technologies Used

- **Python 3.x**
- **Tkinter:** Desktop GUI.
- **SQLite:** Local database storage.
- **Pandas:** Data manipulation.
- **Matplotlib & Seaborn:** Charts and visualizations.
- **Scikit-learn:** Machine learning (linear regression, IsolationForest, KMeans).
- **tkcalendar:** Date selection widgets.

## Project Structure

ExpenseTracker/ 
├── src/ │ 
├── main.py # Main application entry point │ 
├── entry_section.py # Expense entry UI components │
├── analytics_section.py # Analytics and visualization UI │ 
├── database.py # SQLite database management │ 
├── export.py # Data export functions (CSV/Excel) │ 
└── ml.py # Machine learning functions (forecasting, categorization, anomaly detection, etc.) 
├── expense_tracker.db # SQLite database file (created on the first run) 
└── requirements.txt # Python dependencies



## Installation and Running

### Prerequisites

- Python 3.x must be installed.
- `pip` (Python package installer) is required.

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/SmartExpenseTracker.git
   cd SmartExpenseTracker
2. **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
3. Run the Application: Navigate to the src folder and execute:
  ```bash
  cd src
  python main.py
  ```

## How It Works

- **Expense Entry:**
  - Users add expense records via a simple form (date, amount, category, description). Data is stored locally in an SQLite database.

- **Data Analytics:**
  - Users filter data using "From" and "To" date pickers and select an analysis type (Weekly, Monthly, or Yearly). The app resamples the data accordingly and displays:

    - Bar Charts for expense trends.
    - Pie Charts for expense distribution.

- **Forecasting & Budgeting:**
  - The app uses linear regression to forecast future expenses and calculates a recommended monthly budget based on historical data.

- **Anomaly Detection:**
  - New expenses are compared against historical data; if an expense is significantly higher than normal, it is flagged as an anomaly.

- **Additional Insights:**
  - The app provides further analysis by categorizing expenses (Must, Need, Want) and showing cumulative expense trends over time.
