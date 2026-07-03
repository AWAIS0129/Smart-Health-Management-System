from django.db import models
from user_account_manager.models import User
from datetime import datetime
# Create your models here.

class Inference(models.Model):
    
    class InferenceChoices(models.TextChoices):
        Risk_Analysis = 'RA', "Risk Analysis"
        Anomaly_Detection = "AD", "Anomaly Detection"
        Risk_Labeling = "RL","Risk Labeling"
            
    class InferenceParameters(models.TextChoices):
        BP = "BP","BLood Pressure"
        Blood_Sugar = "BS", 'Blood Sugar'
        
        
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    model_name = models.CharField(blank=False, max_length=50)
    model_version = models.CharField(max_length=20)
    inference_type = models.CharField(max_length=2, choices=InferenceChoices.choices)
    inference_results = models.JSONField(blank=True, null=True)
    
    
    parameter_for_inference = models.CharField(max_length=2, choices = InferenceParameters.choices)
    
    class Meta:
        
        ordering = ['-timestamp']
        
        
        indexes = [
                models.Index(fields=['user', '-timestamp']),  
                models.Index(fields=['inference_type']),      
                    ]
            
    def __str__(self):
        return f" {self.user.email} -  {self.get_inference_type_display()}, {self.timestamp}"
    
    