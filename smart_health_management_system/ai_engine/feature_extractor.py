from abc import ABC, abstractmethod
from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from .utils import Calculate_BMI, CalculateAge
from health_data_manager.models import BloodSugar, Weight, BP, HealthProfile
import numpy as np
class FeatureExtractor(ABC):
    
    @abstractmethod
    def extract_features(self, request):
        pass
    
    
class BPFeatureExtractor(FeatureExtractor):
    
    def extract_features(self, request: HttpRequest):
        print("success from feature extractor")
        return f"BP Feature Extraction working for {request}"
    

class BloodSugarFeatureExtractor(FeatureExtractor):
    
    def extract_features(self,request:HttpRequest):
        
        try:
            self.diastolic_bp = BP.objects.get(
                user = request.user,
                is_recent = True
            ).diastolic_blood_pressure
        except ObjectDoesNotExist: 
            
            print(f"No BP reading for {request.user}")
            self.diastolic_bp = 0
        
        
        
        try:
            self.fasting_glucose = BloodSugar.objects.get(
                user = request.user,
                is_recent = True,
                is_deleted = False,
                reading_type = "F"
                
            ).blood_sugar_reading_mgdl
        
        except ObjectDoesNotExist:
            print(f"No Blood sugar reading exists for {request.user}")
            self.fasting_glucose = 0
        
        
        
        try:
            self.weight = Weight.objects.get(
                user = request.user,
                is_recent = True,
                is_deleted = False
            ).weight_in_kg
            
        except ObjectDoesNotExist:
            print(f"No weight reading for {request.user}")
            self.weight = 0
        
        
        try:
            self.height = HealthProfile.objects.get(
                user = request.user,
                is_recent = True,
                is_deleted = False
            ).height_in_meters
            
        except ObjectDoesNotExist:
            print(f"No height recorded for {request.user}")
            self.height = 0
        
        if self.weight > 0 and self.height > 0 :
            self.BMI = Calculate_BMI(
                self.weight,
                self.height
            )
        else:
            self.BMI = 0
        
        
        self.date_of_birth = request.user.date_of_birth
        
        
        self.Age = CalculateAge(self.date_of_birth)
        
        arr =  [self.fasting_glucose, self.diastolic_bp, self.BMI, self.Age]
        print(f"it is raw arr{arr}")
        features_array = np.array(arr).reshape(1, -1)
        print(features_array)
        return features_array
        
    