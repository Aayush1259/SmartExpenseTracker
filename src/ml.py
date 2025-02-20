import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans

def forecast_expenses(data: pd.DataFrame, periods: int = 1):
    if data.empty:
        return pd.DataFrame(columns=["date", "forecast"])
    df = data.copy()
    df.set_index("date", inplace=True)
    monthly = df.resample("M").sum().reset_index()
    monthly["month_num"] = np.arange(len(monthly))
    X = monthly[["month_num"]]
    y = monthly["amount"]
    model = LinearRegression()
    model.fit(X, y)
    future = pd.DataFrame(np.arange(len(monthly), len(monthly)+periods), columns=["month_num"])
    pred = model.predict(future)
    last_date = monthly["date"].max()
    future_dates = pd.date_range(last_date + pd.offsets.MonthBegin(1), periods=periods, freq="M")
    return pd.DataFrame({"date": future_dates, "forecast": pred})

def categorize_expense(description: str):
    texts = [
        "lunch restaurant food dinner",
        "uber taxi bus transport",
        "rent apartment housing",
        "electricity water utilities",
        "movie cinema entertainment",
        "doctor hospital healthcare",
        "books school education",
        "shopping mall clothes shopping",
        "insurance policy insurance",
        "miscellaneous"
    ]
    labels = ["Food", "Transport", "Housing", "Utilities", "Entertainment",
              "Healthcare", "Education", "Shopping", "Insurance", "Other"]
    vec = TfidfVectorizer()
    X_train = vec.fit_transform(texts)
    clf = MultinomialNB()
    clf.fit(X_train, labels)
    X_input = vec.transform([description])
    return clf.predict(X_input)[0]

def fraud_detection(new_amount: float, hist: pd.Series) -> bool:
    if hist.empty or len(hist) < 10:
        mean, std = hist.mean(), hist.std()
        return new_amount > mean + 2*std if std else False
    X = hist.values.reshape(-1,1)
    iso = IsolationForest(contamination=0.05, random_state=0)
    iso.fit(X)
    return iso.predict([[new_amount]])[0] == -1

def personalized_budget_recommendation(data: pd.DataFrame):
    if data.empty:
        return None
    data["date"] = pd.to_datetime(data["date"])
    monthly = data.set_index("date").resample("M").sum()
    avg = monthly["amount"].mean()
    return avg * 0.9 if avg else None

def smart_expense_insights(data: pd.DataFrame) -> str:
    if data.empty:
        return "No data available."
    total = data["amount"].sum()
    top_cat = data.groupby("category")["amount"].sum().idxmax()
    monthly = data.set_index(pd.to_datetime(data["date"])).resample("M").sum()
    avg_monthly = monthly["amount"].mean() if not monthly.empty else 0
    return f"Total: ${total:,.2f}, Top: {top_cat}, Avg(Month): ${avg_monthly:,.2f}"

def spending_categories(data: pd.DataFrame) -> dict:
    mapping = {
       "Must": ["Housing", "Utilities", "Food", "Transport"],
       "Need": ["Healthcare", "Insurance", "Education"],
       "Want": ["Entertainment", "Shopping", "Other"]
    }
    cat_dict = {"Must": 0, "Need": 0, "Want": 0}
    for _, row in data.iterrows():
        cat = row["category"]
        amt = row["amount"]
        if cat in mapping["Must"]:
            cat_dict["Must"] += amt
        elif cat in mapping["Need"]:
            cat_dict["Need"] += amt
        else:
            cat_dict["Want"] += amt
    return cat_dict

def balance_trend(data: pd.DataFrame) -> pd.DataFrame:
    data = data.sort_values("date")
    data["cumulative"] = data["amount"].cumsum()
    return data[["date", "cumulative"]]

def expense_splitter(expense_list):
    if not expense_list:
        return 0, [], []
    X = np.array(expense_list).reshape(-1, 1)
    kmeans = KMeans(n_clusters=2, n_init=10, random_state=0).fit(X)
    labels = kmeans.labels_
    total = np.sum(expense_list)
    eq_share = total / len(expense_list)
    diffs = [amt - eq_share for amt in expense_list]
    return eq_share, diffs, labels
