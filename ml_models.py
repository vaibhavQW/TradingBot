# ml_models.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from database import fetch_all_trades
from logger import log_message


def prepare_ml_data():
    """
    Prepare data for machine learning model.
    """
    # Fetch historical trade data
    trades = fetch_all_trades()
    df = pd.DataFrame(
        trades,
        columns=[
            "id",
            "symbol",
            "quantity",
            "entry_price",
            "target_price",
            "stop_loss",
            "order_id",
            "timestamp",
        ],
    )

    # Feature engineering
    df["price_diff"] = df["target_price"] - df["entry_price"]
    df["risk"] = df["stop_loss"] / df["entry_price"]
    df["reward"] = df["price_diff"] / df["entry_price"]

    # Label: 1 if target reached, 0 if stop-loss triggered
    df["label"] = df["reward"].apply(
        lambda x: 1 if x >= 0.02 else 0
    )  # Example: Success if reward >= 2%

    # Drop rows with missing values
    df = df.dropna()

    return df


def train_ml_model():
    """
    Train a machine learning model to predict trade success.
    """
    df = prepare_ml_data()
    if df.empty:
        log_message("WARNING", "No data available for training ML model.")
        return None

    X = df[["entry_price", "target_price", "stop_loss", "price_diff", "risk", "reward"]]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    log_message("INFO", f"ML Model trained with accuracy: {accuracy * 100:.2f}%")

    return model


def predict_trade_success(model, trade_info):
    """
    Predict the success of a trade using the trained ML model.
    """
    if not model:
        log_message("WARNING", "ML model not trained. Cannot predict trade success.")
        return False

    # Prepare feature vector
    entry_price = trade_info["entry_price"]
    target_price = trade_info["target_price"]
    stop_loss = trade_info["stop_loss"]
    price_diff = target_price - entry_price
    risk = stop_loss / entry_price
    reward = price_diff / entry_price

    features = pd.DataFrame(
        [
            {
                "entry_price": entry_price,
                "target_price": target_price,
                "stop_loss": stop_loss,
                "price_diff": price_diff,
                "risk": risk,
                "reward": reward,
            }
        ]
    )

    prediction = model.predict(features)[0]
    return bool(prediction)  # True for success, False for failure
