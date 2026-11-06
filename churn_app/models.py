from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    CustomerID = models.AutoField(primary_key=True)
    Gender = models.CharField(max_length=10)
    SeniorCitizen = models.BooleanField()
    Partner = models.BooleanField()
    Dependents = models.BooleanField()
    Tenure = models.IntegerField()
    PhoneService = models.BooleanField()
    MultipleLines = models.CharField(max_length=20)
    InternetService = models.CharField(max_length=20)
    OnlineSecurity = models.BooleanField()
    OnlineBackup = models.BooleanField()
    DeviceProtection = models.BooleanField()
    TechSupport = models.BooleanField()
    StreamingTV = models.BooleanField()
    StreamingMovies = models.BooleanField()
    Contract = models.CharField(max_length=20)
    PaperlessBilling = models.BooleanField()
    PaymentMethod = models.CharField(max_length=50)
    MonthlyCharges = models.DecimalField(max_digits=10, decimal_places=2)
    TotalCharges = models.DecimalField(max_digits=10, decimal_places=2)
    churn = models.BooleanField()
    
    def __str__(self):
        return f"Customer {self.CustomerID} - Churn: {self.churn}"
    
def new_customer(customer_data):
    """
    Create a new customer record in the database.
    
    :param customer_data: A dictionary containing customer attributes.
    :return: The created Customer instance.
    """
    customer = Customer.objects.create(
        CustomerID=customer_data.get('CustomerID'),
        Gender=customer_data.get('Gender'),
        SeniorCitizen=customer_data.get('SeniorCitizen'),
        Partner=customer_data.get('Partner'),
        Dependents=customer_data.get('Dependents'),
        Tenure=customer_data.get('Tenure'),
        PhoneService=customer_data.get('PhoneService'),
        MultipleLines=customer_data.get('MultipleLines'),
        InternetService=customer_data.get('InternetService'),
        OnlineSecurity=customer_data.get('OnlineSecurity'),
        OnlineBackup=customer_data.get('OnlineBackup'),
        DeviceProtection=customer_data.get('DeviceProtection'),
        TechSupport=customer_data.get('TechSupport'),
        StreamingTV=customer_data.get('StreamingTV'),
        StreamingMovies=customer_data.get('StreamingMovies'),
        Contract=customer_data.get('Contract'),
        PaperlessBilling=customer_data.get('PaperlessBilling'),
        PaymentMethod=customer_data.get('PaymentMethod'),
        MonthlyCharges=customer_data.get('MonthlyCharges'),
        TotalCharges=customer_data.get('TotalCharges'),
        churn=customer_data.get('churn')
    )
    return customer