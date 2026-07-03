from .notifier import  BloodSugarNotifier, BPNotifier
from .Ai_models import BPAIModel, BloodSugarAIModel
from .result_parser import ResultParser, BloodSugarResultParser
from .feature_extractor import  BloodSugarFeatureExtractor, BPFeatureExtractor
from .ai_engine import AIEngine


class AIEngineFactory:
    
    @staticmethod 
    def create_BP_engine():
        
        return AIEngine(
            ai_model= BPAIModel(),
            result_parser = ResultParser(),
            feature_extractor = BPFeatureExtractor(),
            
        )
        
        
    @staticmethod
    def create_Blood_sugar_engine():
        return AIEngine(
            ai_model= BloodSugarAIModel(),
            result_parser = BloodSugarResultParser(),
            feature_extractor = BloodSugarFeatureExtractor(),
            
        )