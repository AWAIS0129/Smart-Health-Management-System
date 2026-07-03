
class UnitConverter:
    
    @staticmethod
    def lbs_to_kg(weight_lbs: float) -> float:
        return round(float(weight_lbs) / 2.20462, 2)
    
    @staticmethod
    def kg_to_lbs(weight_kg: float) -> float:
        return round(float(weight_kg) * 2.20462, 2)
    
    @staticmethod
    def fahrenheit_to_celsius(temp_f: float) -> float:
        return round((float(temp_f) - 32) * (5/9), 2)
    
    @staticmethod
    def celsius_to_fahrenheit(temp_c: float) -> float:
        return round((float(temp_c) * 9/5) + 32, 2)

