from django import forms
from datetime import date



class HealthReportForm(forms.Form):
    """Form for generating health reports with metric selection and date range."""
    date_class = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm'
    checkbox_class = 'h-5 w-5 rounded border-gray-300 text-green-600 focus:ring-green-500 mr-3'
    checkbox_styles =  'width: 1.25rem; height: 1.25rem;'
    
    # Date range fields
    start_date = forms.DateField(
        label='Start Date',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': date_class,
            'required': True
        })
    )
    end_date = forms.DateField(
        label='End Date',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': date_class,
            'required': True,
            'max':date.today().isoformat()
            
        })
    )
    
    # Health metrics checkboxes
    include_blood_pressure = forms.BooleanField(
        
        label='Blood Pressure (Systolic/Diastolic)',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': checkbox_class,'style':checkbox_styles})
    )
    
    include_blood_sugar = forms.BooleanField(
        label='Blood Sugar (Random & Fasting)',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': checkbox_class,'style':checkbox_styles})

    )
    
    include_weight = forms.BooleanField(
        label='Weight',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': checkbox_class,'style':checkbox_styles})

    )
    
    include_temperature = forms.BooleanField(
        label='Temperature',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': checkbox_class,'style':checkbox_styles})
   )
    
    include_pulse = forms.BooleanField(
        label='Pulse/Heart Rate',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': checkbox_class,'style':checkbox_styles})

    )
    
    include_exercise = forms.BooleanField(
        label='Exercise Duration',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': checkbox_class,'style':checkbox_styles})

    )
    
    include_sleep = forms.BooleanField(
        label='Sleep Duration',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': checkbox_class,'style':checkbox_styles})

    )
    
    include_stress = forms.BooleanField(
        label='Stress Level',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': checkbox_class,'style':checkbox_styles})

    )
    
    include_health_profile = forms.BooleanField(
        label='Health Profile Summary',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': checkbox_class,'style':checkbox_styles})

    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        # Validate date range
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("Start date must be before end date.")
        
        # Ensure at least one metric is selected
        metrics = [
            'include_blood_pressure',
            'include_blood_sugar',
            'include_weight',
            'include_temperature',
            'include_pulse',
            'include_exercise',
            'include_sleep',
            'include_stress',
            'include_health_profile'
        ]
        
        if not any(cleaned_data.get(metric) for metric in metrics):
            raise forms.ValidationError("Please select at least one health metric to include in the report.")
        
        return cleaned_data
    
class ExportCSVForm(HealthReportForm):
   include_health_profile = None