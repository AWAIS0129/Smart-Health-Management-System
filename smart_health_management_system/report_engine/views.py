import csv
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

from .forms import HealthReportForm, ExportCSVForm
from .pdf_generator import HealthReportPDF
from health_data_manager.models import BP, Weight, BloodSugar, Temperature, Pulse, ExerciseDuration, SleepTime, StressLevel, HealthProfile
   
  




@login_required
def generate_report(request):
    
    if request.method == "POST":
        form = HealthReportForm(request.POST)
        if form.is_valid():
            try:
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                
                if isinstance(start_date, str):
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if isinstance(end_date, str):
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                
                pdf_gen = HealthReportPDF(request.user)
                pdf_gen.add_header(start_date, end_date)
                
                if form.cleaned_data['include_health_profile']:
                    profile = HealthProfile.objects.filter(
                        user=request.user,
                        is_deleted=False
                    ).latest('timestamp')
                    pdf_gen.add_health_profile_section(profile)
                
                if form.cleaned_data['include_blood_pressure']:
                    bp_data = BP.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    pdf_gen.add_blood_pressure_section(bp_data)
                
                if form.cleaned_data['include_blood_sugar']:
                    sugar_data = BloodSugar.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    pdf_gen.add_blood_sugar_section(sugar_data)
                
                if form.cleaned_data['include_weight']:
                    weight_data = Weight.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    pdf_gen.add_weight_section(weight_data)
                
                if form.cleaned_data['include_temperature']:
                    temp_data = Temperature.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    pdf_gen.add_temperature_section(temp_data)
                
                if form.cleaned_data['include_pulse']:
                    pulse_data = Pulse.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    pdf_gen.add_pulse_section(pulse_data)
                
                if form.cleaned_data['include_exercise']:
                    exercise_data = ExerciseDuration.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    pdf_gen.add_exercise_section(exercise_data)
                
                if form.cleaned_data['include_sleep']:
                    sleep_data = SleepTime.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    pdf_gen.add_sleep_section(sleep_data)
                
                if form.cleaned_data['include_stress']:
                    stress_data = StressLevel.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    pdf_gen.add_stress_section(stress_data)
                
                pdf_buffer = pdf_gen.generate()
                
                response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
                filename = f"health_report_{start_date}_{end_date}.pdf"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                
                return response
                
            except HealthProfile.DoesNotExist:
                messages.warning(request, "Health profile not found. Please complete your health profile first.")
                return redirect('report_engine:generate_report')
            except Exception as e:
                messages.error(request, f"Error generating report: {str(e)}")
                return redirect('report_engine:generate_report')
        else:
            messages.error(request, "Please correct the form errors")
            return redirect('report_engine:generate_report')
    else:
        form = HealthReportForm()
    
    return render(request, 'report_engine/generate_report.html', {'form': form})


@login_required
def report_home(request):
    return render(request, 'report_engine/report_home.html')




@login_required
def export_csv(request):
    if request.method == "POST":
        
        form = ExportCSVForm(request.POST)
        if form.is_valid():
            
            try:
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="health_data_{start_date}_to_{end_date}.csv"'
                
                writer = csv.writer(response)
                
                header_row = ['Date']
                
                if form.cleaned_data['include_blood_pressure']:
                    header_row.extend(['systolic_blood_pressure', 'diastolic_blood_pressure'])
                
                if form.cleaned_data['include_blood_sugar']:
                    header_row.extend(['blood_sugar_reading_mgdl', 'reading_type'])
                
                if form.cleaned_data['include_weight']:
                    header_row.extend(['Weight_in_kg'])
                
                if form.cleaned_data['include_temperature']:
                    header_row.extend(['temperature_reading_in_celsius'])
                
                if form.cleaned_data['include_pulse']:
                    header_row.extend(['pulse'])
                
                if form.cleaned_data['include_exercise']:
                    header_row.extend(['exercise_duration_in_minutes'])
                
                if form.cleaned_data['include_sleep']:
                    header_row.extend(['Sleep_in_hours'])
                
                if form.cleaned_data['include_stress']:
                    header_row.extend(['stress_level'])
                
                writer.writerow(header_row)
                
                all_data = {}  
                
                
                if form.cleaned_data['include_blood_pressure']:
                    bp_data = BP.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    
                    for record in bp_data:
                        date_str = record.timestamp.date().isoformat()
                        if date_str not in all_data:
                            all_data[date_str] = []
                        
                        
                        entry = {
                            'type': 'bp',
                            'bp_systolic': record.systolic_blood_pressure,
                            'bp_diastolic': record.diastolic_blood_pressure,
                        }
                        all_data[date_str].append(entry)
                
                if form.cleaned_data['include_blood_sugar']:
                    sugar_data = BloodSugar.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    
                    for record in sugar_data:
                        date_str = record.timestamp.date().isoformat()
                        if date_str not in all_data:
                            all_data[date_str] = []
                        
                        entry = {
                            'type': 'sugar',
                            'sugar_value': record.blood_sugar_reading_mgdl,
                            'sugar_type': record.reading_type,
                        }
                        all_data[date_str].append(entry)
                
                if form.cleaned_data['include_weight']:
                    weight_data = Weight.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    
                    for record in weight_data:
                        date_str = record.timestamp.date().isoformat()
                        if date_str not in all_data:
                            all_data[date_str] = []
                        
                        entry = {
                            'type': 'weight',
                            'weight': record.weight_in_kg,
                        }
                        all_data[date_str].append(entry)
                
                if form.cleaned_data['include_temperature']:
                    temp_data = Temperature.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    
                    for record in temp_data:
                        date_str = record.timestamp.date().isoformat()
                        if date_str not in all_data:
                            all_data[date_str] = []
                        
                        entry = {
                            'type': 'temperature',
                            'temperature': record.temperature_reading_celsius,
                        }
                        all_data[date_str].append(entry)
                
                if form.cleaned_data['include_pulse']:
                    pulse_data = Pulse.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    
                    for record in pulse_data:
                        date_str = record.timestamp.date().isoformat()
                        if date_str not in all_data:
                            all_data[date_str] = []
                        
                        entry = {
                            'type': 'pulse',
                            'pulse': record.pulse_reading,
                        }
                        all_data[date_str].append(entry)
                
                if form.cleaned_data['include_exercise']:
                    exercise_data = ExerciseDuration.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    
                    for record in exercise_data:
                        date_str = record.timestamp.date().isoformat()
                        if date_str not in all_data:
                            all_data[date_str] = []
                        
                        entry = {
                            'type': 'exercise',
                            'exercise': record.exercise_duration_in_minutes,
                        }
                        all_data[date_str].append(entry)
                
                if form.cleaned_data['include_sleep']:
                    sleep_data = SleepTime.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    
                    for record in sleep_data:
                        date_str = record.timestamp.date().isoformat()
                        if date_str not in all_data:
                            all_data[date_str] = []
                        
                        entry = {
                            'type': 'sleep',
                            'sleep': record.sleep_duration_hours,
                        }
                        all_data[date_str].append(entry)
                
                if form.cleaned_data['include_stress']:
                    stress_data = StressLevel.objects.filter(
                        user=request.user,
                        is_deleted=False,
                        timestamp__date__range=[start_date, end_date]
                    ).order_by('timestamp')
                    
                    for record in stress_data:
                        date_str = record.timestamp.date().isoformat()
                        if date_str not in all_data:
                            all_data[date_str] = []
                        
                        entry = {
                            'type': 'stress',
                            'stress': record.level,
                        }
                        all_data[date_str].append(entry)
                
                
                # Write data 
                row_count = 0
                for date in sorted(all_data.keys()):
                    entries = all_data[date]
                    
                    # Write each entry 
                    for entry in entries:
                        row = [date]
                        
                        if form.cleaned_data['include_blood_pressure']:
                            if entry.get('type') == 'bp':
                                row.extend([
                                    entry.get('bp_systolic', 'NaN'),
                                    entry.get('bp_diastolic', 'NaN'),
                                ])
                            else:
                                row.extend(['NaN', 'NaN'])  
                        
                        if form.cleaned_data['include_blood_sugar']:
                            if entry.get('type') == 'sugar':
                                row.extend([
                                    entry.get('sugar_value', 'NaN'),
                                    entry.get('sugar_type', 'NaN'),
                                ])
                            else:
                                row.extend(['NaN', 'NaN'])
                        
                        if form.cleaned_data['include_weight']:
                            if entry.get('type') == 'weight':
                                row.extend([entry.get('weight', 'NaN')])
                            else:
                                row.extend(['NaN'])
                        
                        if form.cleaned_data['include_temperature']:
                            if entry.get('type') == 'temperature':
                                row.extend([entry.get('temperature', 'NaN')])
                            else:
                                row.extend(['NaN'])
                        
                        if form.cleaned_data['include_pulse']:
                            if entry.get('type') == 'pulse':
                                row.extend([entry.get('pulse', 'NaN')])
                            else:
                                row.extend(['NaN'])
                        
                        if form.cleaned_data['include_exercise']:
                            if entry.get('type') == 'exercise':
                                row.extend([entry.get('exercise', 'NaN')])
                            else:
                                row.extend(['NaN'])
                        
                        if form.cleaned_data['include_sleep']:
                            if entry.get('type') == 'sleep':
                                row.extend([entry.get('sleep', 'NaN')])
                            else:
                                row.extend(['NaN'])
                        
                        if form.cleaned_data['include_stress']:
                            if entry.get('type') == 'stress':
                                row.extend([entry.get('stress', 'NaN')])
                            else:
                                row.extend(['NaN'])
                        
                        writer.writerow(row)
                        row_count += 1
                
                return response
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                messages.error(request, f'Error exporting data: {str(e)}')
                return redirect('report_engine:export_csv')
    
    else:   
        form = ExportCSVForm()
        return render(request, 'report_engine/export_csv.html', {'form': form})


# 