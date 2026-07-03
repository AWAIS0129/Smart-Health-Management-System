from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# Create your models here.

class TimeSeriesBaseModel(models.Model):
    user = models.ForeignKey("user_account_manager.User", on_delete=models.CASCADE)
    is_recent = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['is_deleted', '-timestamp']),
        ]

class HealthProfile(TimeSeriesBaseModel):
    class Gender(models.TextChoices):
        male =  'm', 'Male'
        female = 'f', 'Female'
        other = 'o', 'Other'
    gender = models.CharField(max_length=10, choices=Gender.choices)
    height_in_meters = models.FloatField(blank=False)
    is_smoker = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Health Profile - {self.user.email} ({self.timestamp.date()})"

    class Meta:
        verbose_name_plural = "Health Profiles"

class Disability(TimeSeriesBaseModel):
    class DisabilityType(models.TextChoices):
        visual = 'V','Visual Impairment'
        hearing = 'H','Hearing Impairment'
        mobility = 'M','Mobility Impairment'
        cognitive = 'C','Cognitive Impairment'
        other = 'O','Other'
    disability_type = models.CharField(max_length=20, choices=DisabilityType.choices)
    
    def __str__(self):
        return f"{self.get_disability_type_display()} - {self.user.email}"
    
    class Meta:
        verbose_name_plural = "Disabilities"
    

class Weight(TimeSeriesBaseModel):
    weight_in_kg= models.FloatField(
        blank=False,
        validators = [
            MinValueValidator(0.1),
            MaxValueValidator(500.0)
        ]
    )
    
    def __str__(self):
        return f"{self.weight_in_kg} kg - {self.user.email} ({self.timestamp.date()})"
   
    

class BP(TimeSeriesBaseModel):
    systolic_blood_pressure = models.IntegerField(
        validators = [
            MinValueValidator(30),
            MaxValueValidator(300)
        ]
    )
    diastolic_blood_pressure = models.IntegerField(
        validators = [
            MinValueValidator(20),
            MaxValueValidator(300)
        ]
    )
    
    def __str__(self):
        return f"{self.systolic_blood_pressure}/{self.diastolic_blood_pressure} mmHg - {self.user.email}"
    
    class Meta:
        verbose_name = "Blood Pressure"
        verbose_name_plural = "Blood Pressures"


class Pulse(TimeSeriesBaseModel):
    pulse_reading = models.IntegerField(
        validators = [
            MinValueValidator(20),
            MaxValueValidator(300)
        ]
    )
    
    def __str__(self):
        return f"{self.pulse_reading} bpm - {self.user.email}"
    
    

class BloodSugar(TimeSeriesBaseModel):
    class ReadingType(models.TextChoices):
        fasting = 'F','Fasting'
        random = 'R','Random'

    blood_sugar_reading_mgdl = models.IntegerField(
        validators = [
            MinValueValidator(10),
            MaxValueValidator(2000)
        ]
    )
    reading_type = models.CharField(max_length=10, choices=ReadingType.choices)
    
    def __str__(self):
        return f"{self.blood_sugar_reading_mgdl} mg/dL ({self.get_reading_type_display()}) - {self.user.email}"
    
    class Meta:
        verbose_name_plural = "Blood Sugar Readings"
    
    

class Temperature(TimeSeriesBaseModel):
    temperature_reading_celsius = models.FloatField(
        validators = [
            MinValueValidator(0.0),
            MaxValueValidator(200.0)
        ]
    )
    
    def __str__(self):
        return f"{self.temperature_reading_celsius}°C - {self.user.email}"
    

class ExerciseDuration(TimeSeriesBaseModel):

    class ExerciseType(models.TextChoices):
        cardio = 'C','Cardio'
        strength = 'S','Strength Training'
        flexibility = 'F','Flexibility Exercises'
    exercise_duration_in_minutes = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(200.0)
        ]
    )
    type = models.CharField(max_length=20, choices=ExerciseType.choices)
    
    def __str__(self):
        return f"{self.exercise_duration} {self.get_unit_display()} of {self.get_type_display()} - {self.user.email}"
    
    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"
    

   

class SleepTime(TimeSeriesBaseModel):
    sleep_duration_hours = models.FloatField(
        validators = [
            MinValueValidator(0.0),
            MaxValueValidator(14.0)
        ]
    )
    
    def __str__(self):
        return f"{self.sleep_duration_hours}h sleep - {self.user.email}"
    
    class Meta:
        verbose_name = "Sleep Time"
        verbose_name_plural = "Sleep Times"

    

class StressLevel(TimeSeriesBaseModel):
    class Levels(models.TextChoices):
        low= 'L','Low'
        medium = 'M','Medium'
        high = 'H','High'
    level = models.CharField(max_length=10, choices=Levels.choices)
    
    def __str__(self):
        return f"Stress: {self.get_level_display()} - {self.user.email}"
    
    class Meta:
        verbose_name = "Stress Level"
        verbose_name_plural = "Stress Levels"
   





