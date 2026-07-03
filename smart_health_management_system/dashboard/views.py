from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def dashboard(request):
    user = request.user.first_name
    
    return render(request, 'dashboard/index.html',{'username':user})
