

def Calculate_BMI(weight_in_kg:float, height_in_meters: float):
    squared_height = height_in_meters ** 2
    return weight_in_kg/squared_height

def CalculateAge(dob):
    
    from datetime import date
    
    today = date.today()
    age = today.year - dob.year
    
    if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
        age -= 1
        
    return age
    