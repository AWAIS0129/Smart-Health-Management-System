from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from health_data_manager.forms import HealthProfileForm
from health_data_manager.models import HealthProfile, Weight
from .forms import UserRegistrationForm, UserLoginForm

# Create your views here.

def home(request):
    form = UserLoginForm()
  
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:dashboard')
    return render(request, 'user_account_manager/index.html',{'form': form})

def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('user_accounts:set_profile')
    
    return render(request, 'user_account_manager/register.html', {'form': form})

def set_profile(request):
    if not request.user.is_authenticated:
        return redirect('user_accounts:home')
    if request.method == "POST":
        form = HealthProfileForm(request.POST)
        if form.is_valid():
            profile_data = form.save(commit=False)
            profile_data.user = request.user
            profile_data.save()
            
            return redirect('dashboard:dashboard')
        else:
            context = {
                'form':form
            }
            return render(request, 'user_accounts:set_profile.html',context)
    else:
        form = HealthProfileForm()
        context = {
            'form':form
        }
        return render(request, 'user_account_manager/set_profile.html',context)

def logout_user(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
    return redirect('user_accounts:home')

def profile_option(request):
    return render(request, 'user_account_manager/profile_option.html')

def view_profile(request):
    
    health_profile  = HealthProfile.objects.get(
        user = request.user,
        is_deleted = False,
        is_recent = True,
    )
    try:
        weight = Weight.objects.get(
            user = request.user,
            is_recent= True,
            is_deleted = False,
        )
        weight = weight.weight_in_kg
    except:
        weight = "No weight entry"
    
    user_name = request.user.first_name +" "+ request.user.last_name
    
    context={
        'user_name': user_name,
        'gender':health_profile.get_gender_display(),
        'height':health_profile.height_in_meters,
        'smoker':health_profile.is_smoker,
        'disabled':health_profile.is_disabled,
        'created':health_profile.timestamp,
        'weight': weight,
        
    }
    return render(request, 'user_account_manager/view_profile.html',context)


def profile_edit(request):
    if request.method == "POST":
        
        form = HealthProfileForm(request.POST)
        if form.is_valid():
            
            profile_data = form.save(commit=False)
            
            # old profiles deletion logic 
            prev_profiles = HealthProfile.objects.filter(
                user = request.user,
                is_recent = True,
                is_deleted = False
            ).update(
                is_recent = False,
                is_deleted = True,
            )
            
            profile_data.user = request.user
            profile_data.save()
            return redirect('dashboard:dashboard')
        
        else:
            return redirect('user_accounts:profile_edit')
    else:
        form = HealthProfileForm()
        context ={
            'form':form
        }
        return render(request, 'user_account_manager/profile_edit.html',context)


def success(request):
    return render(request, 'user_account_manager/success.html')
