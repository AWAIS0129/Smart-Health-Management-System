from django import forms
from datetime import date

class FilterForm(forms.Form):
    
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'max':date.today().isoformat()
            }),
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'max':date.today().isoformat()
            }),
        required=True
    )

class chartForm(FilterForm):
    chart_type = forms.ChoiceField(
        choices = [
            ('bar', 'Bar chart'),
            ('line', 'Line chart'),
            ('pie', 'Pie chart'),
            ('doughnut', 'Doughnut chart'),
            ('polarArea', 'Polar area chart'),
            ('radar', 'Radar chart'),
        ]
    )


class BP_form(chartForm):
    pass

class weight_form(chartForm):
    pass    

class Blood_sugar_form(chartForm):
    blood_sugar_type = forms.ChoiceField(
        choices=[
            ('fasting', 'Fasting Blood Sugar'),
            ('random','Random Blood Sugar')
        ]
    )
class Exercise_form(chartForm):
    pass
class Temperature_form(chartForm):
    pass

class Pulse_form(chartForm):
    pass

class Sleep_form(chartForm):
    pass

class Stress_form(chartForm):
    pass