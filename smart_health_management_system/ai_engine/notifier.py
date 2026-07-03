from notifications.services import NotificationService
from abc import ABC, abstractmethod

class Notifier(ABC):
    
    @abstractmethod
    def risk_level_notification(self):
        pass
    
    @abstractmethod
    def anomaly_notification(self):
        pass
    
    
class BPNotifier(Notifier):
    
    def risk_level_notification(self,level:str, user):
        
        self.levels = [
            'LOW','MODERATE','HIGH','CRITICAL'
                         ]
        level_U =  level.upper()
        
        
        
        if level_U in self.levels:
            
                
            NotificationService.create_notification(
                user,
                "BP Risk Level",
                f"Your recent BP reading has {level} level",
                level_U,
            )
            
    def anomaly_notification(self, user):
        
        NotificationService.create_notification(
            user,
            "BP Anomaly found",
            "BP Anomaly found",
            priority="HIGH"
        )
        
    def hypertension_risk(self, user):
        
        NotificationService.create_notification(
            user,
            "Hypertension Risk",
            "You are at a risk of hypertension",
            "CRITICAL"
        )
        
        
class BloodSugarNotifier(Notifier):
    
    def risk_level_notification(self,level:str, user):
        
        self.levels = [
            'LOW','MODERATE','HIGH','CRITICAL'
                         ]
        level_U =  level.upper()
        
        
        
        if level_U in self.levels:
            
                
            NotificationService.create_notification(
                user,
                "Blood sugar Risk Level",
                f"Your recent blood sugar reading is at {level} level",
                level_U,
            )
            
    def anomaly_notification(self, user):
        
        NotificationService.create_notification(
            user,
            "Blood Sugar Anomaly found",
            "Blood Sugar Anomaly found",
            priority="HIGH"
        )
        
    def diabetes_risk(self, user):
        
        NotificationService.create_notification(
            user,
            "Diabetes Risk",
            "You are at a risk of diabetes",
            "CRITICAL"
        )
        
            