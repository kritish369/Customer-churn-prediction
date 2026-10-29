import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, root_mean_squared_error, mean_squared_error, mean_absolute_error
# Loading the dataset and analyzing the data
data = pd.read_csv("Telco_Customer_Churn_Dataset  (1).csv")
print(data.describe())
print(data.info())
print(data.head(10))


# Data engineering and Filtering

# TotalCharges is read as text because zero-tenure customers have blank values.
# Data engineering and filtering

data["TotalCharges"] = pd.to_numeric(
    data["TotalCharges"].str.strip().replace("", "0")
)

encoded_features = ["gender", "Partner", "Dependents", "Contract"]

# Find the remaining categorical columns automatically
other_categorical_features = [
    column
    for column in data.select_dtypes(include="object").columns
    if column not in [*encoded_features, "customerID", "Churn"]
]

# Combine all categorical features that need encoding
all_categorical_features = [
    *encoded_features,
    *other_categorical_features
]

encoder = OneHotEncoder(
    sparse_output=False,
    handle_unknown="ignore"
)

encoded_data = pd.DataFrame(
    encoder.fit_transform(data[all_categorical_features]),
    columns=encoder.get_feature_names_out(all_categorical_features),
    index=data.index,
)
print(encoded_data.info())
encoded_data = encoded_data.astype("bool")

# Create X using numerical columns and encoded categorical columns
X = pd.concat(
    [
        data.drop(
            columns=["customerID", "Churn","MonthlyCharges", *all_categorical_features]
        ),
        encoded_data,
    ],
    axis=1,
)

y = data["Churn"]
"""print("--------------------")
print("The info of X")
print(X.describe())
print(X.info())
print("--------------------")
print("The info of y")
print(y.info())
print(y.describe()  )
print("--------------------")"""

# Splitting the dataset into training and testing sets

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

# Training the model
model = LogisticRegression(max_iter=3000,class_weight='balanced')
model.fit(X_train, y_train)


y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

print("Training Accuracy:", accuracy_score(y_train, y_pred_train))
print("Test Accuracy:", accuracy_score(y_test, y_pred_test))

print("Classification Report:")
print(classification_report(y_test, y_pred_test))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_test))