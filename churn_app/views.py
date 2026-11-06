from django.shortcuts import render
import joblib as joblib
import pandas as pd
from churn_app.models import new_customer

# Create your views here.

def index(request):
    with open("models/model_joblib_random_forest", "rb") as f:
        model = joblib.load(f)
    with open("models/encoder_joblib", "rb") as f:      # NEW: the saved OneHotEncoder
        encoder = joblib.load(f)

    prediction = None     
    # NEW: so the template always has a value

    if request.method == "POST":     
        # FIXED: was request == "POST"
        CustomerID = request.POST.get("CustomerID")  # NEW: get CustomerID from the form
        tenure = int(request.POST.get("tenure"))
        TotalCharges = float(request.POST.get("TotalCharges"))
        Contract = request.POST.get("Contract")
        PaperlessBilling = request.POST.get("PaperlessBilling")   # FIXED: was named PaymentMethod
        gender = request.POST.get("gender")
        SeniorCitizen = int(request.POST.get("SeniorCitizen"))    # FIXED: number, not a category
        Haspartner = request.POST.get("Partner")
        Hasdependents = request.POST.get("Dependents")
        PhoneService = request.POST.get("PhoneService")
        MultipleLines = request.POST.get("MultipleLines")
        InternetService = request.POST.get("InternetService")
        OnlineSecurity = request.POST.get("OnlineSecurity")
        OnlineBackup = request.POST.get("OnlineBackup")
        DeviceProtection = request.POST.get("DeviceProtection")
        TechSupport = request.POST.get("TechSupport")
        StreamingTV = request.POST.get("StreamingTV")
        StreamingMovies = request.POST.get("StreamingMovies")

        # MOVED inside the if, and put in the SAME ORDER as training
        # (gender, Partner, Dependents, Contract, then the rest in dataset order)
        categorical_features = pd.DataFrame(
            [[
                gender,
                Haspartner,
                Hasdependents,
                Contract,
                PhoneService,
                MultipleLines,
                InternetService,
                OnlineSecurity,
                OnlineBackup,
                DeviceProtection,
                TechSupport,
                StreamingTV,
                StreamingMovies,
                PaperlessBilling,
            ]],
            columns=[
                "gender", "Partner", "Dependents", "Contract",
                "PhoneService", "MultipleLines", "InternetService",
                "OnlineSecurity", "OnlineBackup", "DeviceProtection",
                "TechSupport", "StreamingTV", "StreamingMovies",
                "PaperlessBilling",
            ],
        )

        # FIXED: the encoder encodes, not the model
        encoded_data = encoder.transform(categorical_features)[0].tolist()

        # Numeric columns first, in training order, then the encoded columns
        features = [SeniorCitizen, tenure, TotalCharges] + encoded_data
        prediction = model.predict([features])[0]  
        # "Yes" or "No"
        # Save the customer data to the database
        customer_data = {
            "CustomerID": CustomerID,
            "Gender": gender,
            "SeniorCitizen": SeniorCitizen,
            "Partner": Haspartner,
            "Dependents": Hasdependents,
            "Tenure": tenure,
            "PhoneService": PhoneService,
            "MultipleLines": MultipleLines,
            "InternetService": InternetService,
            "OnlineSecurity": OnlineSecurity,
            "OnlineBackup": OnlineBackup,
            "DeviceProtection": DeviceProtection,
            "TechSupport": TechSupport,
            "StreamingTV": StreamingTV,
            "StreamingMovies": StreamingMovies,
            "Contract": Contract,
            "PaperlessBilling": PaperlessBilling,
            "PaymentMethod": None,  # Placeholder, as it's not collected from the form
            "MonthlyCharges": None,  # Placeholder, as it's not collected from the form
            "TotalCharges": TotalCharges,
            "churn": prediction   # Store as boolean
        }
        new_customer.objects.create(**customer_data)
        
        

    return render(request, "index.html", {"prediction": prediction})   # FIXED: send it to the template