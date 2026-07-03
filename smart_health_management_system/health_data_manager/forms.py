from . import models
from django import forms

class HealthProfileForm(forms.ModelForm):
    class Meta:
        model = models.HealthProfile
        fields = [
            'gender',
            'height_in_meters',
            'is_smoker',
            'is_disabled',
            'timestamp',
        ]
        widgets = {
            'gender': forms.Select(choices=models.HealthProfile.Gender.choices),
            'height_in_meters': forms.NumberInput(attrs={'step': '0.01'}),
            'is_smoker': forms.CheckboxInput(),
            'is_disabled': forms.CheckboxInput(),
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'})
            }
        

class DisabilityForm(forms.ModelForm):
    class Meta:
        model = models.Disability
        fields = ['disability_type','timestamp']
        widgets = {
            'disability_type': forms.Select(choices=models.Disability.DisabilityType.choices),
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class WeightForm(forms.ModelForm):
    unit = forms.ChoiceField( choices=[('kg', 'Kilograms (kg)'), ('lbs', 'Pounds (lbs)')], required=True)
    class Meta:
        model = models.Weight
        fields = ['weight_in_kg','timestamp']
        labels = {
            'weight_in_kg': 'Weight'
        }
        widgets = {
            'weight_in_kg': forms.NumberInput(
                    attrs={
                    'step': '0.1',
                    'min' : '10',
                    'max':'300',
                    'oninvalid': "this.setCustomValidity('Enter value between 10 kg to 300 kg ')",
                    'oninput': "this.setCustomValidity('')",
                    'required':True
                    }
            ),
            'timestamp': forms.DateTimeInput(
                
                attrs={
                    'type': 'datetime-local',
                    }
                )
        }
        
class WeightEditForm(forms.ModelForm):
   
    class Meta:
        model = models.Weight
        fields = ['weight_in_kg','timestamp']

        widgets = {
            'weight_in_kg': forms.NumberInput(
                    attrs={
                    'step': '0.1',
                    'min' : '10',
                    'max':'300',
                    'oninvalid': "this.setCustomValidity('Enter value between 10 kg  to 300')",
                    'oninput': "this.setCustomValidity('')",
                    'required':True
                    }
            ),
            'timestamp': forms.DateTimeInput(
                
                attrs={
                    'type': 'datetime-local',
                    }
                )
        }

class BPForm(forms.ModelForm):
    class Meta:
        model = models.BP
        fields = ['systolic_blood_pressure', 'diastolic_blood_pressure','timestamp']
        widgets = {
            'systolic_blood_pressure': forms.NumberInput(
                attrs={
                    'step': '1',
                    'min' : '30',
                    'max':'300',
                    'oninvalid': "this.setCustomValidity('Enter value between 30 mm//hg to 300 mm/hg')",
                    'oninput': "this.setCustomValidity('')",
                    'required':'True'
                    }
                ),
            'diastolic_blood_pressure': forms.NumberInput(
                 attrs={
                    'step': '1',
                    'min' : '20',
                    'max':'300',
                    'oninvalid': "this.setCustomValidity('Enter value between 20 mm/hg to 300 mm/hg')",
                    'oninput': "this.setCustomValidity('')",
                    'required':'True'
                    }
            ),
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class PulseForm(forms.ModelForm):
    class Meta:
        model = models.Pulse
        fields = ['pulse_reading','timestamp']
        widgets = {
            'pulse_reading': forms.NumberInput(
                    attrs={
                    'step': '1',
                    'min' : '20',
                    'max':'300',
                    'oninvalid': "this.setCustomValidity('Enter value between 20 and 300')",
                    'oninput': "this.setCustomValidity('')",
                    'required':'True'
                    }
            ),
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'})
            
        }

class BloodSugarForm(forms.ModelForm):
    class Meta:
        model = models.BloodSugar
        fields = ['blood_sugar_reading_mgdl', 'reading_type','timestamp']
        labels = {
            'blood_sugar_reading_mgdl':'Blood Sugr Reading'
        }
        widgets = { 
            'blood_sugar_reading_mgdl': forms.NumberInput(
                     attrs={
                    'step': '1',
                    'min' : '10',
                    'max':'2000',
                    'oninvalid': "this.setCustomValidity('Enter value between 10 mg/dl to 2000 mg/dl')",
                    'oninput': "this.setCustomValidity('')",
                    'required':'True'
                    }
            ),
            'reading_type': forms.Select(choices=models.BloodSugar.ReadingType.choices),
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class TemperatureForm(forms.ModelForm):
    unit = forms.ChoiceField( choices=[('C', 'celsius'), ('F', 'farenheit')], required=True)
    class Meta:
        model = models.Temperature
        fields = ['temperature_reading_celsius','timestamp']
        labels={
            'temperature_reading_celsius':'Temperature Reading'
        }
        widgets = {
            'temperature_reading': forms.NumberInput(
                    attrs={
                    'step': '0.1',
                    'min' : '20',
                    'max':'50',
                    'oninvalid': "this.setCustomValidity('Enter value between 20 and 50 Celsius')",
                    'oninput': "this.setCustomValidity('')",
                    'required':'True',
                    'id': 'temperature-input'
                    }
            ),
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
class TemperatureEditForm(forms.ModelForm):
    class Meta:
        model = models.Temperature
        fields = ['temperature_reading_celsius','timestamp']
        labels={
            'temperature_reading_celsius':'Temperature Reading'
        }
        widgets = {
            'temperature_reading': forms.NumberInput(
                    attrs={
                    'step': '0.1',
                    'min' : '20',
                    'max':'50',
                    'oninvalid': "this.setCustomValidity('Enter value between 20 and 50 Celsius')",
                    'oninput': "this.setCustomValidity('')",
                    'required':'True',
                    'id': 'temperature-input'
                    }
            ),
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = models.ExerciseDuration
        fields = ['exercise_duration_in_minutes', 'type','timestamp']
        widgets = {
            'type': forms.Select(choices=models.ExerciseDuration.ExerciseType.choices),
            'exercise_duration_in_minutes': forms.NumberInput(
                    attrs={
                    'step': '0.1',
                    'min' : '0.1',
                    'max':'200',
                    'oninvalid': "this.setCustomValidity('Enter value between 0 and 200')",
                    'oninput': "this.setCustomValidity('')",
                    'required':'True'
                    }
            ),
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class SleepTimeForm(forms.ModelForm):
    class Meta:
        model = models.SleepTime
        fields = ['sleep_duration_hours','timestamp']
        labels = {
            'sleep_duration_hours':'Sleep in hours'
        }
        widgets = {
            'sleep_duration_hours': forms.NumberInput(
                    attrs={
                    'step': 'any',
                    'min' : '0.5',
                    'max':'14.0',
                    'oninvalid': "this.setCustomValidity('Enter value between 0.1 hours to 16.0 hours')",
                    'oninput': "this.setCustomValidity('')",
                    'required':True
                    }
            ),
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class StressLevelForm(forms.ModelForm):
    class Meta:
        model = models.StressLevel
        fields = ['level','timestamp']
        widgets = {
            'level': forms.Select(choices=models.StressLevel.Levels.choices),
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class FileUploadForm(forms.Form):
    uploaded_file = forms.FileField(
        label="Choose File",
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer',
            'accept': '.csv, .xlsx, .xls'
        })
    )