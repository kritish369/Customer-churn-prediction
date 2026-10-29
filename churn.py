
import pandas as pd

from sklearn.preprocessing import OneHotEncoder, LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

# 1. Load the dataset
data = pd.read_csv("Telco_Customer_Churn_Dataset  (1).csv")

# 2. Convert TotalCharges to numeric
data["TotalCharges"] = pd.to_numeric(
    data["TotalCharges"].str.strip().replace("", "0")
)

# 3. Identify categorical features
encoded_features = [
    "gender",
    "Partner",
    "Dependents",
    "Contract"
]

other_categorical_features = [
    column
    for column in data.select_dtypes(include="object").columns
    if column not in [
        *encoded_features,
        "customerID",
        "Churn",
        "PaymentMethod"
    ]
]

all_categorical_features = [
    *encoded_features,
    *other_categorical_features
]

# 4. One-hot encode categorical features
encoder = OneHotEncoder(
    sparse_output=False,
    handle_unknown="ignore"
)

encoded_data = pd.DataFrame(
    encoder.fit_transform(data[all_categorical_features]),
    columns=encoder.get_feature_names_out(
        all_categorical_features
    ),
    index=data.index
)

# 5. Build X and y
X = pd.concat(
    [
        data.drop(
            columns=[
                "customerID",
                "Churn",
                "MonthlyCharges",
                "PaymentMethod",
                *all_categorical_features
            ]
        ),
        encoded_data
    ],
    axis=1
)

y = data["Churn"]

# 6. Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 7. Define the models
models = {
    "Logistic Regression": LogisticRegression(
        max_iter=3000,
        class_weight="balanced"
    ),

    "Decision Tree": DecisionTreeClassifier(
        class_weight="balanced",
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    )
}

# 8. Train and evaluate each model
results = []

for name, model in models.items():
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # Probabilities for ROC-AUC
    y_probability = model.predict_proba(X_test)[:, 
        list(model.classes_).index("Yes")
    ]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(
        y_test, y_pred, pos_label="Yes", zero_division=0
    )
    recall = recall_score(
        y_test, y_pred, pos_label="Yes", zero_division=0
    )
    f1 = f1_score(
        y_test, y_pred, pos_label="Yes", zero_division=0
    )
    roc_auc = roc_auc_score(
        (y_test == "Yes").astype(int),
        y_probability
    )

    print("Accuracy:", round(accuracy, 4))
    print("Churn Precision:", round(precision, 4))
    print("Churn Recall:", round(recall, 4))
    print("Churn F1-score:", round(f1, 4))
    print("ROC-AUC:", round(roc_auc, 4))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred, labels=["No", "Yes"]))

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Churn Precision": precision,
        "Churn Recall": recall,
        "Churn F1-score": f1,
        "ROC-AUC": roc_auc
    })

# 9. Compare all models
results_df = pd.DataFrame(results)

print("\n\nMODEL COMPARISON")
print(
    results_df
    .sort_values("Churn F1-score", ascending=False)
    .round(4)
    .to_string(index=False)
)

