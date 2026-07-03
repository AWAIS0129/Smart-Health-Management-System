from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError, ObjectDoesNotExist


from . import models
from . import forms
from .services import save_entry_to_db, save_file_data, mark_new_recent, Notifications
from .utils import UnitConverter



@login_required
def mode(request):
    return render(request, 'health_data_manager/mode_selection.html')


@login_required
def operations(request):
    return render(request, 'health_data_manager/operations.html')


@login_required
def manual_entry(request):
    return render(request, 'health_data_manager/manual_health_data_entry.html')


@login_required
def file_upload(request):
    message = None
    error = None
    
    if request.method == "POST":
        form = forms.FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['uploaded_file']
            try:
                save_file_data(uploaded_file, request)
                message = f"File {uploaded_file.name} uploaded and processed successfully!"
                messages.success(request, message)
            except ValidationError as e:
                messages.error(request, "Validation Failed")
            except Exception as e:
                messages.error(request, f"Error while processing file")
                
        else:
            messages.error(request,"Error")
    else:
        form = forms.FileUploadForm()
    
    context = {'form': form, 'error': error}
    return render(request, 'health_data_manager/file_upload.html', context)


@login_required
def blood_pressure(request):

    if request.method == "POST":
        
        form = forms.BPForm(request.POST)
        
        if form.is_valid():
            
            try:
                
                save_entry_to_db(models.BP, form, request)
                messages.success(request, "Blood pressure data saved successfully")
                Notifications.BP_saved_successfully_notification(request)

                
                return redirect('health_data_manager:BP')
            
            except ValidationError as e:
                
                messages.error(request, f"Validation error: {str(e)}")
                return redirect('health_data_manager:BP')
                
            except Exception as e:
                
            
                messages.error(request, "Error saving blood pressure data")
                return redirect('health_data_manager:BP')
                
        else:
            
            messages.error(request, "Invalid Data, Please fill al fields with valid data")
            return render(request, 'health_data_manager/BP.html', {'form': form})   
            
    else:
        form = forms.BPForm()
        return render(request, 'health_data_manager/BP.html', {'form': form})


@login_required
def blood_sugar(request):
    
    if request.method == "POST":
        form = forms.BloodSugarForm(request.POST)
        
        if form.is_valid():

            
            try:
                
                save_entry_to_db(models.BloodSugar,form, request)
                messages.success(request, "Blood sugar data saved successfully")
                Notifications.blood_sugar_saved_successfully_notification(request)                
                return redirect('health_data_manager:blood_sugar')
            
            
            except ValidationError as e:
                messages.error(request, f"Validation error: {str(e)}")
                return redirect('health_data_manager:blood_sugar')
            
            except Exception as e:
                messages.error(request, "Error saving blood sugar data")
                return redirect('health_data_manager:blood_sugar')
        else:
            messages.error(request, "Invalid Data, Please fill in all the fields with valid input")
            return redirect('health_data_manager:blood_sugar')
        
    else:
        form = forms.BloodSugarForm()
        return render(request, 'health_data_manager/blood_sugar.html', {'form': form})


@login_required
def weight(request):
    
    
    if request.method == "POST":
        
        form = forms.WeightForm(request.POST)
        
        if form.is_valid():
            
            
            try:
                unit = request.POST.get("unit")
                
                weight_value = form.cleaned_data.get("weight_in_kg")
                
                weight_in_kg = None
                
                if unit.lower() == "lbs":
                    weight_in_kg = UnitConverter.lbs_to_kg(weight_value)
                else:
                    weight_in_kg = weight_value
                
                
                
                # Update form data with normalized weight
                data = form.cleaned_data
                data['weight_in_kg'] = weight_in_kg
                new_form = forms.WeightForm(data)
                
                if new_form.is_valid():
                    try:
                        save_entry_to_db(models.Weight,new_form,request)
                        messages.success(request, "Weight data saved successfully")
                        Notifications.Weight_saved_successfully_notification(request)
                        return redirect('health_data_manager:weight')
                    
                    except ValidationError as e:
                        messages.error(request, f"Validation error: {str(e)}")
                        return redirect('health_data_manager:weight')
                        
                    except Exception as e:
                        messages.error(request, "Error saving weight data")
                        return redirect('health_data_manager:weight')
                    
                else:
                    messages.error(request, "Error converting weight data")
                    return redirect('health_data_manager:weight')
            except ValidationError as e:
                        messages.error(request, f"Validation error: {str(e)}")
                        return redirect('health_data_manager:weight')
                
                
                    
        else:
            messages.error(request, "Invalid Data, Please fill al fields with valid data")
            return redirect('health_data_manager:weight')
    else:
        form = forms.WeightForm()
        return render(request, 'health_data_manager/weight.html', {'form': form})


@login_required
def temperature(request):
    
    if request.method == "POST":
        
        form = forms.TemperatureForm(request.POST)
        
        if form.is_valid():
            try:
                
                unit = form.cleaned_data.get("unit")
                reading = form.cleaned_data.get("temperature_reading_celsius")
                new_reading = None
                
                if unit.upper() == "F":
                    new_reading = UnitConverter.fahrenheit_to_celsius(reading)
                else:
                    new_reading = reading
                    
                
                data = form.cleaned_data
                data['temperature_reading_celsius'] = new_reading
                new_form = forms.TemperatureForm(data)
                
                if new_form.is_valid():
                    
                        save_entry_to_db(models.Temperature, new_form,request)
                        messages.success(request, "Temperature saved successfully")
                        Notifications.Temperature_saved_successfully_notification(request)
                        return redirect("health_data_manager:temperature")
                else:
                    messages.error(request, f"Invalid Data, Please fill all fields with valid values")
                    return redirect("health_data_manager:temperature")


                
                
            except ValidationError as e:
                messages.error(request, f"Validation error: {str(e)}")
                return redirect("health_data_manager:temperature")
            except Exception as e:
                messages.error(request, "Error saving temperature")
                return redirect("health_data_manager:temperature")
    else:
        form = forms.TemperatureForm()
        return render(request, 'health_data_manager/temperature.html', {'form': form})


@login_required
def pulse(request):
    form = forms.PulseForm()
    
    if request.method == "POST":
        form = forms.PulseForm(request.POST)
        
        if form.is_valid():
            try:
                save_entry_to_db(models.Pulse,form, request)
                messages.success(request, "Pulse data saved successfully")
                Notifications.Pulse_saved_successfully_notification(request)
                return redirect('health_data_manager:pulse')
            except ValidationError as e:
                messages.error(request, f"Validation error: {str(e)}")
                return redirect('health_data_manager:pulse')
            except Exception as e:
                messages.error(request, "Error saving pulse data")
                return redirect('health_data_manager:pulse')
        else:
            messages.error(request, "Invalid Data, Please fill all the fields with valid data")
            return redirect('health_data_manager:pulse')
            
    else:
        return render(request, 'health_data_manager/pulse.html', {'form': form})


@login_required
def exercise(request):
    
    if request.method == "POST":
        form = forms.ExerciseForm(request.POST)
        if form.is_valid():
            try:
                save_entry_to_db(models.ExerciseDuration,form, request)
                messages.success(request, "Exercise data saved successfully")
                Notifications.Exercise_saved_successfully_notification(request)
                return redirect('health_data_manager:exercise')
            except ValidationError as e:
                messages.error(request, f"Validation error: {str(e)}")
                return redirect('health_data_manager:exercise')
            except Exception as e:
                messages.error(request, "Error saving exercise data")
                return redirect('health_data_manager:exercise')
        
        else:
            messages.error(request, "Invalid Data, Please fill al fields with valid data")
            return redirect('health_data_manager:exercise')
            
            
    else:
        form = forms.ExerciseForm()
        return render(request, 'health_data_manager/exercise.html', {'form': form})

    


@login_required
def sleep(request):
    
    
    if request.method == "POST":
        form = forms.SleepTimeForm(request.POST)
        if form.is_valid():
            try:
                save_entry_to_db(models.SleepTime,form, request)
                messages.success(request, "Sleep data saved successfully")
                Notifications.Sleep_saved_successfully_notification(request)
                return redirect('health_data_manager:sleep')
            except ValidationError as e:
                messages.error(request, f"Validation error: {str(e)}")
                return redirect('health_data_manager:sleep')
            except Exception as e:
                messages.error(request, "Error saving sleep data")
                return redirect('health_data_manager:sleep')
        else:
            messages.error(request, "Invalid Data, Please fill al fields with valid data")
            return redirect('health_data_manager:sleep')
    else:
        form = forms.SleepTimeForm()
        return render(request, 'health_data_manager/sleep.html', {'form': form})


@login_required
def stress(request):
    
    if request.method == "POST":
        form = forms.StressLevelForm(request.POST)
        if form.is_valid():
            try:
                save_entry_to_db(models.StressLevel,form, request)
                messages.success(request, "Stress level recorded successfully")
                Notifications.Stress_saved_successfully_notification(request)
                return redirect('health_data_manager:stress')
            except ValidationError as e:
                messages.error(request, f"Validation error: {str(e)}")
                return redirect('health_data_manager:stress')
            except Exception as e:
                messages.error(request, "Error saving stress level")
                return redirect('health_data_manager:stress')
        else:
            messages.error(request, "Please Select valid option")
            return redirect('health_data_manager:stress')
        
    else:
        form = forms.StressLevelForm()
        
        return render(request, 'health_data_manager/stress.html', {'form': form})


@login_required
def edit_health_data(request):
    
    return render(request, 'health_data_manager/edit_parameters/edit_base.html')



@login_required
def edit_bp(request, obj_id:int = None):
    
    
    if not  obj_id:
        data = models.BP.objects.filter(
            user = request.user,
            is_deleted = False
        ).order_by('-timestamp')
        context = {
            'data': data
        }
        return render(request, 'health_data_manager/edit_parameters/edit_bp.html', context)
    
    else:
        
        
        try:
        
            data = models.BP.objects.get(
                user = request.user,
                id = obj_id,
                is_deleted = False,
                
            )
            
        except ObjectDoesNotExist:
            messages.error(request,"Record not found")
            return redirect('health_data_manager:edit_bp')
        
        
        delete_request = request.GET.get('delete')
        if delete_request:
            
            was_recent = data.is_recent
            
            data.is_deleted = True
            data.save()
            
            if was_recent:
                
                mark_new_recent(models.BP,obj_id,request.user.id)
                
            messages.success(request, "Record deleted successfully")
            return redirect('health_data_manager:edit_bp')
            
            
        if request.method == "POST":
            form = forms.BPForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,"Data updated successfully")
                return redirect('health_data_manager:edit_bp')
            else:
                messages.error(request,"Unable to save the data due to error")
                return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_bp_form.html', {'form': form})
        

        
        else:
            form = forms.BPForm(instance=data)
            context = {
            'form':form
            }
            return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_bp_form.html', context)
        
        
        
        
        
        
@login_required
def edit_weight(request, obj_id:int = None):
    
    
    if not  obj_id:
        data = models.Weight.objects.filter(
            user = request.user,
            is_deleted = False
        ).order_by('-timestamp')
        context = {
            'data': data
        }
        return render(request, 'health_data_manager/edit_parameters/edit_weight.html', context)
    
    else:
        
        
        try:
        
            data = models.Weight.objects.get(
                user = request.user,
                id = obj_id,
                is_deleted = False,
                
            )
            
        except ObjectDoesNotExist:
            messages.error(request,"Record not found")
            return redirect('health_data_manager:edit_weight')
        
        
        delete_request = request.GET.get('delete')
        if delete_request:
            was_recent = data.is_recent
            
            data.is_deleted = True
            data.save()
            
            if was_recent:
                
                mark_new_recent(models.Weight,obj_id,request.user.id)
            messages.success(request, "Record deleted successfully")
            return redirect('health_data_manager:edit_weight')
            
            
        if request.method == "POST":
            form = forms.WeightEditForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,"Data updated successfully")
                return redirect('health_data_manager:edit_weight')
            else:
                messages.error(request,"Unable to save the data due to error")
                return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_weight_form.html', {'form': form})
        

        
        else:
            form = forms.WeightEditForm(instance=data)
            context = {
            'form':form
            }
            return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_weight_form.html', context)
        
        
        
@login_required
def edit_sugar(request, obj_id:int = None):
    
    
    if not  obj_id:
        data = models.BloodSugar.objects.filter(
            user = request.user,
            is_deleted = False
        ).order_by('-timestamp')
        context = {
            'data': data
        }
        return render(request, 'health_data_manager/edit_parameters/edit_sugar.html', context)
    
    else:
        
        
        try:
        
            data = models.BloodSugar.objects.get(
                user = request.user,
                id = obj_id,
                is_deleted = False,
                
            )
            
        except ObjectDoesNotExist:
            messages.error(request,"Record not found")
            return redirect('health_data_manager:edit_sugar')
        
        
        delete_request = request.GET.get('delete')
        if delete_request:
            was_recent = data.is_recent
            
            data.is_deleted = True
            data.save()
            
            if was_recent:
                
                mark_new_recent(models.BloodSugar,obj_id,request.user.id)
            messages.success(request, "Record deleted successfully")
            return redirect('health_data_manager:edit_sugar')
            
            
        if request.method == "POST":
            form = forms.BloodSugarForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,"Data updated successfully")
                return redirect('health_data_manager:edit_sugar')
            else:
                messages.error(request,"Unable to save the data due to error")
                return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_sugar_form.html', {'form': form})
        

        
        else:
            form = forms.BloodSugarForm(instance=data)
            context = {
            'form':form
            }
            return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_sugar_form.html', context)
        
        
        
@login_required
def edit_temperature(request, obj_id:int = None):
    
    
    if not  obj_id:
        data = models.Temperature.objects.filter(
            user = request.user,
            is_deleted = False
        ).order_by('-timestamp')
        context = {
            'data': data
        }
        return render(request, 'health_data_manager/edit_parameters/edit_temperature.html', context)
    
    else:
        
        
        try:
        
            data = models.Temperature.objects.get(
                user = request.user,
                id = obj_id,
                is_deleted = False,
                
            )
            
        except ObjectDoesNotExist:
            messages.error(request,"Record not found")
            return redirect('health_data_manager:edit_temperature')
        
        
        delete_request = request.GET.get('delete')
        if delete_request:
            was_recent = data.is_recent
            
            data.is_deleted = True
            data.save()
            
            if was_recent:
                
                mark_new_recent(models.Temperature,obj_id,request.user.id)
            messages.success(request, "Record deleted successfully")
            return redirect('health_data_manager:edit_temperature')
            
            
        if request.method == "POST":
            form = forms.TemperatureEditForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,"Data updated successfully")
                return redirect('health_data_manager:edit_temperature')
            else:
                messages.error(request,"Unable to save the data due to error")
                return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_temperature_form.html', {'form': form})
        

        
        else:
            form = forms.TemperatureEditForm(instance=data)
            context = {
            'form':form
            }
            return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_temperature_form.html', context)
        
        
        
@login_required
def edit_pulse(request, obj_id:int = None):
    
    
    if not  obj_id:
        data = models.Pulse.objects.filter(
            user = request.user,
            is_deleted = False
        ).order_by('-timestamp')
        context = {
            'data': data
        }
        return render(request, 'health_data_manager/edit_parameters/edit_pulse.html', context)
    
    else:
        
        
        try:
        
            data = models.Pulse.objects.get(
                user = request.user,
                id = obj_id,
                is_deleted = False,
                
            )
            
        except ObjectDoesNotExist:
            messages.error(request,"Record not found")
            return redirect('health_data_manager:edit_pulse')
        
        
        delete_request = request.GET.get('delete')
        if delete_request:
            was_recent = data.is_recent
            
            data.is_deleted = True
            data.save()
            
            if was_recent:
                
                mark_new_recent(models.Pulse,obj_id,request.user.id)
            messages.success(request, "Record deleted successfully")
            return redirect('health_data_manager:edit_pulse')
            
            
        if request.method == "POST":
            form = forms.PulseForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,"Data updated successfully")
                return redirect('health_data_manager:edit_pulse')
            else:
                messages.error(request,"Unable to save the data due to error")
                return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_pulse_form.html', {'form': form})
        

        
        else:
            form = forms.PulseForm(instance=data)
            context = {
            'form':form
            }
            return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_pulse_form.html', context)



        
        
@login_required
def edit_exercise(request, obj_id:int = None):
    
    
    if not  obj_id:
        data = models.ExerciseDuration.objects.filter(
            user = request.user,
            is_deleted = False
        ).order_by('-timestamp')
        context = {
            'data': data
        }
        return render(request, 'health_data_manager/edit_parameters/edit_exercise.html', context)
    
    else:
        
        
        try:
        
            data = models.ExerciseDuration.objects.get(
                user = request.user,
                id = obj_id,
                is_deleted = False,
                
            )
            
        except ObjectDoesNotExist:
            messages.error(request,"Record not found")
            return redirect('health_data_manager:edit_exercise')
        
        
        delete_request = request.GET.get('delete')
        if delete_request:
            was_recent = data.is_recent
            
            data.is_deleted = True
            data.save()
            
            if was_recent:
                
                mark_new_recent(models.ExerciseDuration,obj_id,request.user.id)
            messages.success(request, "Record deleted successfully")
            return redirect('health_data_manager:edit_exercise')
            
            
        if request.method == "POST":
            form = forms.ExerciseForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,"Data updated successfully")
                return redirect('health_data_manager:edit_exercise')
            else:
                messages.error(request,"Unable to save the data due to error")
                return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_exercise_form.html', {'form': form})
        

        
        else:
            form = forms.ExerciseForm(instance=data)
            context = {
            'form':form
            }
            return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_exercise_form.html', context)
        
        
@login_required
def edit_sleep(request, obj_id:int = None):
    
    
    if not  obj_id:
        data = models.SleepTime.objects.filter(
            user = request.user,
            is_deleted = False
        ).order_by('-timestamp')
        context = {
            'data': data
        }
        return render(request, 'health_data_manager/edit_parameters/edit_sleep.html', context)
    
    else:
        
        
        try:
        
            data = models.SleepTime.objects.get(
                user = request.user,
                id = obj_id,
                is_deleted = False,
                
            )
            
        except ObjectDoesNotExist:
            messages.error(request,"Record not found")
            return redirect('health_data_manager:edit_sleep')
        
        
        delete_request = request.GET.get('delete')
        if delete_request:
            was_recent = data.is_recent
            
            data.is_deleted = True
            data.save()
            
            if was_recent:
                
                mark_new_recent(models.SleepTime,obj_id,request.user.id)
            messages.success(request, "Record deleted successfully")
            return redirect('health_data_manager:edit_sleep')
            
            
        if request.method == "POST":
            form = forms.SleepTimeForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,"Data updated successfully")
                return redirect('health_data_manager:edit_sleep')
            else:
                messages.error(request,"Unable to save the data due to error")
                return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_sleep_form.html', {'form': form})
        

        
        else:
            form = forms.SleepTimeForm(instance=data)
            context = {
            'form':form
            }
            return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_sleep_form.html', context)
        
        
@login_required
def edit_stress(request, obj_id:int = None):
    
    
    if not  obj_id:
        data = models.StressLevel.objects.filter(
            user = request.user,
            is_deleted = False
        ).order_by('-timestamp')
        context = {
            'data': data
        }
        return render(request, 'health_data_manager/edit_parameters/edit_stress.html', context)
    
    else:
        
        
        try:
        
            data = models.StressLevel.objects.get(
                user = request.user,
                id = obj_id,
                is_deleted = False,
                
            )
            
        except ObjectDoesNotExist:
            messages.error(request,"Record not found")
            return redirect('health_data_manager:edit_stress')
        
        
        delete_request = request.GET.get('delete')
        if delete_request:
            was_recent = data.is_recent
            
            data.is_deleted = True
            data.save()
            
            if was_recent:
                
                mark_new_recent(models.StressLevel,obj_id,request.user.id)
            messages.success(request, "Record deleted successfully")
            return redirect('health_data_manager:edit_stress')
            
            
        if request.method == "POST":
            form = forms.StressLevelForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,"Data updated successfully")
                return redirect('health_data_manager:edit_stress')
            else:
                messages.error(request,"Unable to save the data due to error")
                return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_stress_form.html', {'form': form})
        

        
        else:
            form = forms.StressLevelForm(instance=data)
            context = {
            'form':form
            }
            return render(request, 'health_data_manager/edit_parameters/edit_forms/edit_stress_form.html', context)






