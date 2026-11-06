# Customer Churn Predictor

A Django web app that predicts whether a telecom customer is likely to churn. The user fills in a form with the customer's details, and a trained scikit-learn model returns **Yes** (likely to churn) or **No** (likely to stay).

The project has two parts:

1. **Training** (`models/churn.py`): trains and compares four classifiers on the Telco Customer Churn dataset, then saves the best one.
2. **Web app** (Django): loads the saved model and serves a form that returns predictions.

---

## Project structure

```
saiket systems/
├── data/
│   └── Telco_Customer_Churn_Dataset.csv
├── models/
│   ├── churn.py                  # training + evaluation script
│   └── artifacts/                # created by churn.py
│       ├── churn_model.joblib
│       ├── encoder.joblib
│       └── metadata.joblib
└── churn_site/                   # Django project (name may differ)
    ├── manage.py
    ├── churn_site/
    │   └── settings.py
    └── predictor/                # Django app
        ├── views.py
        ├── templates/
        │   └── index.html
        └── static/
            └── css/
                └── style.css
```

---

## Requirements

- Python 3.10 or newer
- pandas
- scikit-learn
- joblib
- Django

```bash
pip install pandas scikit-learn joblib django
```

> **Important:** train the model and run Django in the **same environment**. A model saved with one scikit-learn version can fail or behave differently under another.

---

## 1. Train the model

Run the script from the `models` folder:

```bash
cd "/path/to/saiket systems/models"
python churn.py
```

The script:

- loads the dataset from `../data/`
- converts `TotalCharges` to numbers
- one-hot encodes the categorical features
- splits the data 80/20 (stratified)
- trains Logistic Regression, Decision Tree, Random Forest and Gradient Boosting
- prints accuracy, churn precision, recall, F1, ROC-AUC, the classification report and the confusion matrix for each
- saves the best model (by churn F1-score), the encoder and the metadata to `models/artifacts/`

---

## 2. Run the web app

Run Django from the folder that contains `manage.py`:

```bash
cd "/path/to/saiket systems/churn_site"
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

### Django setup checklist

- `"predictor"` is listed in `INSTALLED_APPS` in `settings.py`.
- The view is connected to a URL in `urls.py`, for example `path("", views.index, name="index")`.
- `index.html` is at `predictor/templates/index.html`.
- `style.css` is at `predictor/static/css/style.css`.
- If `static/` is at the project root instead of inside the app, add:
  ```python
  STATIC_URL = "/static/"
  STATICFILES_DIRS = [BASE_DIR / "static"]
  ```
- The paths in `views.py` point to the three `.joblib` files.

---

## How a prediction works

1. The user submits the form, and the browser sends a POST request.
2. The view reads the values from `request.POST` (all strings).
3. Numeric fields are converted: `tenure` to `int`, `TotalCharges` to `float`, `SeniorCitizen` to `int` (0 or 1).
4. Categorical fields stay as strings and go into a one-row table with the same column names used in training.
5. The saved **encoder** converts them to 0/1 columns with `encoder.transform(...)`. It never calls `fit` again.
6. The numeric and encoded columns are joined in the same order as training: `SeniorCitizen`, `tenure`, `TotalCharges`, then the encoded columns.
7. The saved **model** returns `"Yes"` or `"No"` with `model.predict(...)`.
8. The view renders `index.html` with `prediction` in the context.

---

## Form fields

| Field | Type | Values sent |
|---|---|---|
| `tenure` | number | 0 to 72 (months) |
| `TotalCharges` | number | dollars |
| `SeniorCitizen` | radio | `1` or `0` |
| `gender` | select | `Female`, `Male` |
| `Partner` | radio | `Yes`, `No` |
| `Dependents` | radio | `Yes`, `No` |
| `Contract` | select | `Month-to-month`, `One year`, `Two year` |
| `PaperlessBilling` | radio | `Yes`, `No` |
| `PhoneService` | radio | `Yes`, `No` |
| `MultipleLines` | select | `No`, `Yes`, `No phone service` |
| `InternetService` | select | `DSL`, `Fiber optic`, `No` |
| `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies` | select | `No`, `Yes`, `No internet service` |

`MonthlyCharges` and `PaymentMethod` are not used by the model, so they are not in the form.

The form's option values match the dataset spelling exactly. Do not change their capitalization or wording: an unseen value is silently encoded as all zeros (`handle_unknown="ignore"`) and gives a wrong prediction.

---

## Troubleshooting

| Problem | Likely cause and fix |
|---|---|
| `FileNotFoundError` for the CSV | Check the folder layout and the filename. Use a path based on `Path(__file__)`, and remove any trailing `/` after `.csv`. |
| `can't open file 'manage.py'` | You are in the wrong folder. Run `find ~/Desktop -name manage.py` and `cd` into that folder. |
| `cd` fails on a folder with a space | Quote the path: `cd "/Users/you/Desktop/saiket systems"`. |
| CSS not loading | Check `STATICFILES_DIRS`, the `static/css/style.css` path and `{% load static %}`. Hard refresh with Cmd+Shift+R. `DEBUG` must be `True` on the dev server. |
| `ValueError: could not convert string to float` | The model received raw text. Encode the categorical fields with the saved encoder first. |
| Predictions look wrong | Check the column order, the exact category spelling, and that the model and encoder come from the same training run. |
| `ImportError` for `joblib` from `sklearn.externals` | Use `import joblib`. |
| `unexpected keyword argument 'ps_label'` | Typo. It should be `pos_label`. |

---

## Notes and limitations

- The model is trained on one dataset and is a learning project, not a production system.
- The prediction is a probability-based estimate. Do not use it alone for real business decisions.
- For a cleaner setup, a scikit-learn `Pipeline` with a `ColumnTransformer` would let you save one object that encodes and predicts in a single call.
