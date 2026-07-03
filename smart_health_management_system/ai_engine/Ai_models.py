from abc import ABC, abstractmethod
import joblib 
from pathlib import Path
from django.conf import settings
from .models import Inference
import json



class AIModel(ABC):
    
    @abstractmethod
    def load_model(self):
        pass
    
    @abstractmethod
    
    def predict(self, features):
        pass
    
    
class BloodSugarAIModel(AIModel):
    def __init__(self):
        self.MODEL_PATH = Path(settings.BASE_DIR)/'ai_engine'/'ml_models'/'diabetes_models'/'risk_prediction_model'/'diabetes_logistic_regression_model.pkl'
        self.SCALER_PATH = Path(settings.BASE_DIR)/'ai_engine'/'ml_models'/'diabetes_models'/'risk_prediction_model'/'diabetes_logistic_regression_scaler.pkl'
        self.model_name = 'Diabetes Model'
        self.model_version =  '1.0'
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        try:
            self.model = joblib.load(self.MODEL_PATH)
            self.scaler = joblib.load(self.SCALER_PATH)
            print('Model and scaler loaded successfully')
        except FileNotFoundError as err:
            self.model = None
            self.scaler = None
            print(f"Model or scaler not found at {self.MODEL_PATH} and {self.SCALER_PATH} respectively: {err}")
        except Exception as err:
            self.model = None
            self.scaler = None
            print(f"An error occurred during model loading: {err}")
        
            
    
    def predict(self, features):
        if self.scaler is None or self.model is None:

            return f"model or scalar not laded successfully"
        

        self.scaled_features = self.scaler.transform(features)
        print(f"it is scaled arr {self.scaled_features}")
        
        self.raw_probability = self.model.predict_proba(self.scaled_features)
        self.raw_outcome = self.model.predict(self.scaled_features)
        
        self.probability = float(self.raw_probability[0][1])
        self.outcome = int(self.raw_outcome[0])
        
        print(f"probability:{self.probability}")
        
        self.raw_result = {
            "probability": self.probability,
            "outcome":self.outcome
        }
        print(self.raw_result)
        
        return self.raw_result
    



class BPAIModel(AIModel):
    
    def load_model(self):
        return f"Blood Sugar AI Model loaded"
    
    def predict(self, features):
        print("success from blood sugar model")
        return f"It is Blood Sugar AI model prediction's raw data for {features}"