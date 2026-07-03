from django.db import transaction
from django.core.exceptions import ValidationError
from .files_handler import process_file
from notifications.services import NotificationService
from django.core.exceptions import ObjectDoesNotExist



    
class Notifications:
    @staticmethod
    def BP_saved_successfully_notification(request):
        NotificationService.create_notification(
            request.user,
            "BP reading added",
            "Blood pressure saved successfully",
            "LOW,"
        )
        
    @staticmethod
    def Weight_saved_successfully_notification(request):
        NotificationService.create_notification(
            request.user,
            "Weight reading added",
            "New weight reading saved successfully",
            "LOW,"
        )
        
    @staticmethod
    def Temperature_saved_successfully_notification(request):
        NotificationService.create_notification(
            request.user,
            "Temperature reading added",
            "New temperature reading saved successfully",
            "LOW,"
        )
    @staticmethod
    def Pulse_saved_successfully_notification(request):
        NotificationService.create_notification(
            request.user,
            "Pulse reading added",
            "New Pulse reading saved successfully",
            "LOW,"
        )
    @staticmethod
    def Exercise_saved_successfully_notification(request):
        NotificationService.create_notification(
            request.user,
            "Exercise reading added",
            "New exercise duration reading saved successfully",
            "LOW,"
        )
    @staticmethod      
    def Sleep_saved_successfully_notification(request):
        NotificationService.create_notification(
            request.user,
            "Sleep reading added",
            "New sleep reading saved successfully",
            "LOW,"
        )
        
    @staticmethod
    def Stress_saved_successfully_notification(request):
        NotificationService.create_notification(
            request.user,
            "Stress reading added",
            "New stress level reading saved successfully",
            "LOW,"
        )
    @staticmethod
    def blood_sugar_saved_successfully_notification(request):
        NotificationService.create_notification(
            request.user,
            "Blood Glucose reading added",
            "Blood Glucose reading saved successfully",
            "LOW,"
        )
    
    
    



def get_user_id(request):
    
    if not request.user.is_authenticated:
        raise PermissionError("User must be authenticated")
    return request.user.id


def save_entry_to_db(model, form, request):
    
    try:
        if not request.user.is_authenticated:
            raise PermissionError("User must be authenticated to save data")
        
        with transaction.atomic():
            obj = form.save(commit=False)
            obj.user_id = get_user_id(request)
            inverse_is_recent(model, request)
            obj.save()
            return True
            
    except PermissionError:
        raise PermissionError
    except Exception as e:
        raise PermissionError


def save_file_data(file_uploaded, request):
    try:
        if not request.user.is_authenticated:
            raise PermissionError("User must be authenticated to upload files")
        process_file(file_uploaded, request)
        
    except ValidationError as e:
        raise ValidationError
    except Exception as e:
        raise Exception
    
    
def inverse_is_recent(model, request):
    try:
        model.objects.filter(
            user = request.user.id,
            is_recent = True
        ).update(
            is_recent = False
        )
    except:
        raise ObjectDoesNotExist
    
    
def mark_new_recent(model,obj_id,user):
     
    # Find the next most recent record (not deleted, not the current one)
    next_recent = model.objects.filter(
        user = user,
        is_deleted=False
    ).exclude(
        id=obj_id
    ).order_by('-timestamp', "-id").first()
    
    # If there is another record, mark it as recent
    if next_recent:
        next_recent.is_recent = True
        next_recent.save()
        
    current_record = model.objects.get(
        user = user,
        id = obj_id
    )
    
    current_record.is_recent = False
    current_record.save()
    return
