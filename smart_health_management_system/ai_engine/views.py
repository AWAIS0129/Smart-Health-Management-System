from django.shortcuts import render, redirect
from .ai_factory import AIEngineFactory
from .models import Inference
import json


# Create your views here.


def home(request):
    result = None
    try:
        inference = Inference.objects.filter(user=request.user).latest('timestamp')
        result = json.loads(inference.inference_results)
    except Inference.DoesNotExist:
        print(f"No Inference result for {request.user}")
    
    context = {
        'result': result
    }
    return render(request, "ai_engine/home.html", context)

def infer(request):
    engine = AIEngineFactory.create_Blood_sugar_engine()
    engine.predict(request)
    return redirect('ai_engine:home')
