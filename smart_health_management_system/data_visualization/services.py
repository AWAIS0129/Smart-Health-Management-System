from django.utils.timezone import localtime
import json



def get_context_for_chart(data, field, lower=0, upper=0, chart_type = None,unit =None):
    labels = [localtime(reading.timestamp).strftime('%Y-%m-%d %H:%M') for reading in data]
    values = [getattr(reading,field) for reading in data]
    
    
    chart_data = {
        'chart_type':chart_type,
        'labels': labels,
        'values':values,
        'lower_value':lower,
        'upper_value' : upper,
        'unit':unit,
        
    }

    context = {
        'chart_data': json.dumps(chart_data)  
    }
    return context


def get_context_for_table(request,custom_form,custom_model):
    
    start_date = None
    end_date = None
    tables_data = None  
    try:
        if request.method == "POST":
            new_form = custom_form(request.POST)
            if new_form.is_valid():
                form_data = new_form.cleaned_data
                start_date = form_data.get('start_date')
                end_date = form_data.get('end_date')
                tables_data = custom_model.objects.filter(
                    user = request.user,
                    is_deleted = False,
                    timestamp__date__range=[start_date,end_date]
                    )
               
        filter_form = custom_form()
        context = {
            'filter_form':filter_form,
            'data':tables_data,
        }
        return context
    except ValueError:
        return "cannot access data"
        
            


