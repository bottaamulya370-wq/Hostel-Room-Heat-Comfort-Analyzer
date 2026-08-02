import pandas as pd
from sklearn.linear_model import LinearRegression


def train_model(df):
    """
    Train a Linear Regression model using Temperature data.
    """

    data = df.copy()

    # Create Time column if it doesn't exist
    if "Time" not in data.columns:
        data["Time"] = range(1, len(data) + 1)

    X = data[["Time"]]
    y = data["Temperature"]

    model = LinearRegression()
    model.fit(X, y)

    return model


def predict_temperature(model, future_time):
    """
    Predict future temperature.
    """
    prediction = model.predict([[future_time]])
    return round(float(prediction[0]), 2)


def model_accuracy(model, df):
    """
    Return model R² score.
    """
    data = df.copy()

    if "Time" not in data.columns:
        data["Time"] = range(1, len(data) + 1)

    X = data[["Time"]]
    y = data["Temperature"]

    return round(model.score(X, y), 2)


def future_dataframe(model, future_time):
    """
    Create prediction dataframe for plotting.
    """

    future = pd.DataFrame({
        "Time": range(1, future_time + 1)
    })

    future["Predicted Temperature"] = model.predict(future)

    return future