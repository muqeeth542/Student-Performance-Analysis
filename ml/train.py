import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv("../data/StudentPerformanceFactors.csv")

features = [
    'Attendance',
    'Hours_Studied',
    'Sleep_Hours',
    'Previous_Scores',
    'Motivation_Level',
    'Tutoring_Sessions'
]
X = df[features]
X = pd.get_dummies(X, drop_first=True)
feature_columns = X.columns

y = df['Exam_Score']


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("R2 Score:", r2)

import pickle

with open("model.pkl", "wb") as f:
    pickle.dump(
        {
            "model": model,
            "features": feature_columns
        },
        f
    )

print("Model and feature columns saved")


