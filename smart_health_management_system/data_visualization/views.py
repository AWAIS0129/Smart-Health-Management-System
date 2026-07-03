from django.shortcuts import render
from .forms import FilterForm, BP_form, weight_form, Blood_sugar_form, Temperature_form, Pulse_form, Sleep_form,Stress_form, Exercise_form
from .services import get_context_for_table, get_context_for_chart

from health_data_manager.models import BP, Weight, BloodSugar,StressLevel,SleepTime,Temperature, Pulse,ExerciseDuration
from health_data_manager import models
import json

# Create your views here.



def home(request):
    return render(request, 'data_visualization/home.html')


def visualization_type(request):
    return render(request,'data_visualization/visualization_type.html')

def tables_home(request):
    return render(request,'data_visualization/tables_home.html')

def choose_option(request):
    return render(request, 'data_visualization/choose_option.html')


def view_bp(request):
    context = get_context_for_table(request,FilterForm,models.BP)

    
    return render(request,'data_visualization/view_bp.html',context)

def view_weight(request):
    context = get_context_for_table(request,FilterForm,models.Weight)

    return render(request,'data_visualization/view_weight.html',context)

def view_sugar(request):
    context = get_context_for_table(request,FilterForm,models.BloodSugar)
    return render(request,'data_visualization/view_sugar.html',context)

def view_temperature(request):
    context = get_context_for_table(request,FilterForm,models.Temperature)
    return render(request,'data_visualization/view_temperature.html',context)

def view_exercise(request):
    context = get_context_for_table(request, FilterForm, models.ExerciseDuration)
    return render(request,'data_visualization/view_exercise.html',context)

def view_sleep(request):
    context = get_context_for_table(request,FilterForm,models.SleepTime)
    return render(request,'data_visualization/view_sleep.html',context)

def view_stress(request):
    context = get_context_for_table(request,FilterForm,models.StressLevel)
    return render(request,'data_visualization/view_stress.html',context)

def view_pulse(request):
    context = get_context_for_table(request,FilterForm,models.Pulse)
    return render(request,'data_visualization/view_pulse.html',context)



def visualize_systolic_BP(request):
    if request.method =="POST":
        form = BP_form(request.POST)

        if form.is_valid():
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            chart_type = request.POST.get('chart_type')
            data = BP.objects.filter(
                user=request.user,
                is_deleted=False,
                timestamp__date__range=[start_date, end_date]
            ).order_by('timestamp')
            lower = 100
            upper = 130
            unit = 'mmHg'
            field = "systolic_blood_pressure"
            context = get_context_for_chart(data,field, lower,upper,chart_type,unit)

    
            return render(request, 'data_visualization/visualize_systolic_BP.html', context)
    else:
        form = BP_form()
        return render(request, 'data_visualization/systolic_bp_plot_form.html',{'form':form})



def visualize_diastolic_BP(request):
  
    if request.method =="POST":
        form = BP_form(request.POST)

        if form.is_valid():
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            chart_type = request.POST.get('chart_type')
            data = BP.objects.filter(
                user=request.user,
                is_deleted=False,
                timestamp__date__range=[start_date, end_date]
            ).order_by('timestamp')
            lower = 70
            upper = 85
            unit = 'mmHg'
            field = "diastolic_blood_pressure"
            context = get_context_for_chart(data,field, lower,upper,chart_type,unit)

    
            return render(request, 'data_visualization/visualize_diastolic_BP.html', context)
    else:
        form = BP_form()
        return render(request, 'data_visualization/diastolic_bp_plot_form.html',{'form':form})









    
 
def visualize_weight(request):
    if request.method == "POST":
        form = weight_form(request.POST)
        if form.is_valid():
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            chart_type = request.POST.get('chart_type')
                    
        # Fetch BP data for current user
        data = Weight.objects.filter(
            user=request.user,
            is_deleted=False,
            timestamp__date__range=[start_date, end_date]
            ).order_by('timestamp')
        field = "weight_in_kg"
        lower = 45
        upper = 70
        unit= 'Kilograms'
        context = get_context_for_chart(data,field,lower,upper,chart_type,unit)
        return render(request, 'data_visualization/visualize_weight.html', context)
    else:
        form = weight_form()
        return render(request, 'data_visualization/weight_plot_form.html',{'form':form})



def visualize_temperature(request):
    if request.method == "POST":
        form = Temperature_form(request.POST)
        if form.is_valid():
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            chart_type = request.POST.get('chart_type')
        data = Temperature.objects.filter(
            user=request.user,
            is_deleted=False,
            timestamp__date__range=[start_date, end_date],
            ).order_by('timestamp')
        lower = 36.1
        upper = 37.2
        field = "temperature_reading_celsius"
        unit = "Celsius"
        context = get_context_for_chart(data,field,lower,upper,chart_type,unit)
        return render(request, 'data_visualization/visualize_temperature.html', context)
    else:
        form = Temperature_form()
        return render(request, 'data_visualization/temperature_plot_form.html', {'form':form})
        



def visualize_blood_sugar(request):
    if request.method =="POST":
        form = Blood_sugar_form(request.POST)
        if form.is_valid():
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            chart_type = request.POST.get('chart_type')
            blood_sugar_type = request.POST.get('blood_sugar_type')
            if blood_sugar_type == "fasting":
                data = BloodSugar.objects.filter(
                    user = request.user,
                    is_deleted = False,
                    reading_type = 'F',
                    timestamp__date__range=[start_date, end_date],
                ).order_by('timestamp')
                lower = "60"
                upper = "90"
            elif blood_sugar_type == "random":
                data = BloodSugar.objects.filter(
                    user = request.user,
                    is_deleted = False,
                    reading_type = 'R',
                    timestamp__date__range=[start_date, end_date],
                ).order_by('timestamp')
                lower = "100"
                upper = "140"

        field = "blood_sugar_reading_mgdl"
        unit = "mg/dl"
    
        context = get_context_for_chart(data,field,lower,upper,chart_type,unit)
        return render(request, 'data_visualization/visualize_blood_sugar.html', context)
    else:
        form = Blood_sugar_form()
        return render(request, 'data_visualization/blood_sugar_plot_form.html', {'form':form})


def visualize_pulse(request):
    if request.method =="POST":
        form = Pulse_form(request.POST)
        if form.is_valid():
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            chart_type = request.POST.get('chart_type')
            unit = "bpm"
            data = Pulse.objects.filter(
                user=request.user,
                is_deleted=False,
                timestamp__date__range=[start_date, end_date],
                ).order_by('timestamp')
            lower = 60
            upper = 100
            field = "pulse_reading"
            context = get_context_for_chart(data,field,lower,upper,chart_type,unit)
            return render(request, 'data_visualization/visualize_pulse.html', context)
    else:
        form = Pulse_form()
        return render(request, 'data_visualization/pulse_plot_form .html', {'form':form})
        


def visualize_exercise(request):
    if request.method == "POST": 
        form = Exercise_form(request.POST)
        if form.is_valid():
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            data = ExerciseDuration.objects.filter(
                user=request.user,
                is_deleted=False,
                timestamp__date__range=[start_date, end_date],
                ).order_by('timestamp')
            field = "exercise_duration_in_minutes"
            chart_type = request.POST.get('chart_type')
            lower = 20
            upper = 100
            units= 'minutes'
            context = get_context_for_chart(data,field,lower, upper,chart_type,units,)
            return render(request, 'data_visualization/visualize_exercise.html', context)  
    else:
        form = Exercise_form()
        return render(request, 'data_visualization/exercise_plot_form.html', {'form':form})



def visualize_sleep(request):
    if request.method == 'POST':
        form = Sleep_form(request.POST)
        if form.is_valid():
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            chart_type = request.POST.get('chart_type')
            unit = "Hours"
            lower = 6
            upper = 8
            data = SleepTime.objects.filter(
                user=request.user,
                is_deleted=False,
                timestamp__date__range=[start_date, end_date],
                ).order_by('timestamp')
            field = "sleep_duration_hours"
            context = get_context_for_chart(data,field,lower,upper,chart_type,unit)
            return render(request, 'data_visualization/visualize_sleep.html', context)
    else:
        form = Sleep_form()
        return render(request, 'data_visualization/sleep_plot_form.html', {'form':form})
        
            
    


def visualize_stress(request):
    if request.method == "POST":
        form = Stress_form(request.POST)
        if form.is_valid:
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            chart_type = request.POST.get('chart_type')
            unit = "levels"
            lower = 6
            upper = 0
            data = StressLevel.objects.filter(
                user=request.user,
                is_deleted=False,
                timestamp__date__range=[start_date, end_date],
                ).order_by('timestamp')
            
            field = "level"
            context = get_context_for_chart(data,field,lower,upper,chart_type,unit)
            return render(request, 'data_visualization/visualize_stress.html', context)
    else:
        form= Stress_form()
        return render(request, 'data_visualization/stress_plot_form.html', {'form':form})



def cumulative_plot(request):
        random_sugar_context = get_context_for_chart(BloodSugar.objects.filter(user=request.user, is_deleted=False, reading_type = "R").order_by('timestamp'),"blood_sugar_reading_mgdl", 100, 140, 'line', 'mg/dl')
        fasting_sugar_context = get_context_for_chart(BloodSugar.objects.filter(user=request.user, is_deleted=False, reading_type = "F").order_by('timestamp'),'blood_sugar_reading_mgdl', 60, 90, 'line', 'mg/dl')
        weight_context = get_context_for_chart(Weight.objects.filter(user=request.user, is_deleted=False).order_by('timestamp'),"weight_in_kg", 45, 70, 'line', 'kg')
        systolic_bp_context = get_context_for_chart(BP.objects.filter(user=request.user, is_deleted=False).order_by('timestamp'),"systolic_blood_pressure", 100, 130, 'line', 'mmHg')
        diastolic_bp_context = get_context_for_chart(BP.objects.filter(user=request.user, is_deleted=False).order_by('timestamp'),"diastolic_blood_pressure", 70, 85, 'line', 'mmHg')

        context = [random_sugar_context,fasting_sugar_context,weight_context,systolic_bp_context,diastolic_bp_context]
        
        
        return render(request, 'data_visualization/cumulative_plot.html',{"context":context})
