
from .Ai_models import AIModel,BPAIModel, BloodSugarAIModel
from django.http import HttpRequest
from .result_parser import ResultParser
from .feature_extractor import FeatureExtractor, BloodSugarFeatureExtractor, BPFeatureExtractor
from .models import Inference
import json


class AIEngine:
    
    def __init__(
        self,
        ai_model:AIModel,
        result_parser:ResultParser,
        feature_extractor:FeatureExtractor
        ):
        self.ai_model = ai_model
        self.result_parser = result_parser
        self.feature_extractor = feature_extractor
        print("success from ai engine initializer or constructor")
        
    def predict(self, request: HttpRequest):
        
        
        
        self.features = self.feature_extractor.extract_features(request)
        self.raw_result = self.ai_model.predict(self.features)
        self.result = self.result_parser.parse(self.raw_result,request)
        self.save_result(request)
        
        self.inference_result.save()
        return self.result
    
    def save_result(self, request):
    
        self.inference_result = Inference.objects.create(
        user = request.user,
        model_name =self.ai_model.model_name,
        model_version =self.ai_model.model_version,
        inference_type= Inference.InferenceChoices.Risk_Analysis,
        inference_results = json.dumps(self.result),
        parameter_for_inference = "Blood Sugar",
        
    )


        
    
    

