from abc import ABC, abstractmethod
from django.http import HttpRequest
from .notifier import Notifier, BloodSugarNotifier, BPNotifier

class ResultParser(ABC):
    @abstractmethod
    def parse(self,raw_result):
        pass
    
    
    
    
class BloodSugarResultParser(ResultParser):
    
    def parse(self, raw_result:dict, request: HttpRequest):
        
        self.probability = raw_result['probability']
        self.outcome = raw_result['outcome']
        self.result = {
            "Diabetes_risk" :None,
            "Diabetes_probability" : None,
            'Diabetes_risk_level': None,
            'Message':None,
            'Recommendation': None
        }
        self.risk_notifier = BloodSugarNotifier()
        
        self.diabetes_risk = "yes" if self.outcome == 1 else "no"
        
        if self.probability >= 0.7:
            self.risk_level = "Very High"
            self.message = "Your results indicate a very high risk for diabetes."
            self.recommendation = "Please consult a healthcare provider immediately."
            self.risk_notifier.diabetes_risk(user = request.user)
            self.risk_notifier.risk_level_notification(level = "critical", user = request.user)
            
        elif self.probability >= 0.5:
            self.risk_level = "High"
            self.message = "Your results show elevated risk factors for diabetes."
            self.recommendation = "Schedule a check-up with your doctor soon."
            self.risk_notifier.diabetes_risk(user = request.user)
            self.risk_notifier.risk_level_notification(level = "high", user = request.user)
            
            
        elif self.probability >= 0.3:
            self.risk_level = "Moderate"
            self.message = "Your results suggest some risk factors for diabetes."
            self.recommendation = "Consider lifestyle changes and monitor your health."
            self.risk_notifier.risk_level_notification(level = "moderate", user = request.user)
            
        elif self.probability >= 0.1:
            self.risk_level = "Low"
            self.message = "Your results show minimal risk factors for diabetes."
            self.recommendation = "Maintain healthy habits and routine check-ups."
            self.risk_notifier.risk_level_notification(level = "low", user = request.user)
            
        else:
            self.risk_level = "Very Low"
            self.message = "Your results show very low risk for diabetes."
            self.recommendation = "Continue your healthy lifestyle."
            
            
        self.result = {
            "Diabetes_risk" :self.diabetes_risk,
            "Diabetes_probability" : self.probability,
            'Diabetes_risk_level': self.risk_level,
            'Message':self.message,
            'Recommendation': self.recommendation
        }
        
        return self.result
        
        
       
    