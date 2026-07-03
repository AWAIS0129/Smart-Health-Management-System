import os
import pandas as pd
from datetime import datetime


allowed_extensions = [
    ".csv",
    ".xlsx",
    ".xls",
]

required_columns = [
    "weight_in_kg",
    "blood_sugar_random",
    "blood_sugar_fasting",
    "systolic_bp",
    "diastolic_bp",
    "date"
]


def validate_file_format(extension):
    if extension in allowed_extensions:
        return True
    else:
        return False
    


def impute_date(df):
    
    if 'date' not in df.columns:
        return df
    
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    df['date'] = df['date'].ffill()
    
    df['date'] = df['date'].bfill()
    
    return df

def make_data_frame(file, extension):
    file.seek(0)
    
    if extension == ".csv":
        return pd.read_csv(file, header=0)

    if extension in [".xlsx", ".xls"]:
        obj =pd.read_excel(file, header=0)
        return obj
    
    else:
        raise ValueError("Unsupported file format")



def validate_dataframe_headers(dframe):
    dataframe_columns = [col.strip().lower() for col in dframe.columns]
    missing_columns = []
    
    
    for column in required_columns:
        if column not in dataframe_columns:
            missing_columns.append(column)
            
    if len(missing_columns) > 0 :
        raise ValueError(f"{missing_columns} is/are missing")
    

  
def get_timestamp(row, df):
    
    if "date" in df.columns and pd.notna(row.get("date")):
        try:
            return pd.to_datetime(row["date"]).strftime("%Y-%m-%dT%H:%M")
        except Exception:
            pass
    return datetime.now().strftime("%Y-%m-%dT%H:%M")
    



def save_dataframe_rows(df, request):
    from . import forms
    from . import models
    from .services import save_entry_to_db

    
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    
    df = impute_date(df)

    for _, row in df.iterrows():

        timestamp = get_timestamp(row, df)
        
        # weight readings extraction and saving
        weight_val = row["weight_in_kg"] if "weight_in_kg" in row else None
        if pd.notna(weight_val) and weight_val is not None:
            
            form = forms.WeightForm({
                "weight_in_kg": float(weight_val) if not pd.isna(weight_val) else None,
                "unit" : 'kg',
                "timestamp": timestamp
            })
            


            if form.is_valid():
                save_entry_to_db(models.Weight, form, request)


        # random blood sugar readings extraction and saving
        sugar_val_random = row["blood_sugar_random"] if "blood_sugar_random" in row else None
        if pd.notna(sugar_val_random) and sugar_val_random is not None:
            form = forms.BloodSugarForm({
                "blood_sugar_reading_mgdl": float(sugar_val_random) if not pd.isna(sugar_val_random) else None,
                "reading_type": "R",
                "timestamp": timestamp
            })
            
            if form.is_valid():
                save_entry_to_db(models.BloodSugar, form, request)
            
        # fasting blood sugar readings extraction and saving
        sugar_val_fasting = row["blood_sugar_fasting"] if "blood_sugar_fasting" in row else None
        if pd.notna(sugar_val_fasting) and sugar_val_fasting is not None:
            form = forms.BloodSugarForm({
                "blood_sugar_reading_mgdl": float(sugar_val_fasting) if not pd.isna(sugar_val_fasting) else None,
                "reading_type": "F",
                "timestamp": timestamp
            })
 

            if form.is_valid():
                save_entry_to_db(models.BloodSugar, form, request)

        # blood pressure readings extraction and saving
        systolic_val = row["systolic_bp"] if "systolic_bp" in row else None
        diastolic_val = row["diastolic_bp"] if "diastolic_bp" in row else None
        
        if (pd.notna(systolic_val) and systolic_val is not None and 
            pd.notna(diastolic_val) and diastolic_val is not None):
            form = forms.BPForm({
                "systolic_blood_pressure": float(systolic_val) if not pd.isna(systolic_val) else None,
                "diastolic_blood_pressure": float(diastolic_val) if not pd.isna(diastolic_val) else None,
                "timestamp": timestamp,
            })


            if form.is_valid():
                save_entry_to_db(models.BP, form, request)   



def process_file(file, request):


    extension = os.path.splitext(file.name)[1].lower()

    if not validate_file_format(extension):
        raise ValueError(f"Invalid file format: {file.name}")
    
    data_frame = make_data_frame(file,extension)

    
    validate_dataframe_headers(data_frame)

    data_frame.columns = data_frame.columns.str.strip().str.lower()
    


    save_dataframe_rows(data_frame, request)
 
    return True