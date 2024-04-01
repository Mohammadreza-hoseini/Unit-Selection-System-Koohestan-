from os import name
import django_filters
from .models import Student, EducationalAssistant


class StudentModelFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'firstname': ['exact'],
            'lastname': ['exact'],
            'gender': ['exact'],
            'student_number': ['exact'],
            'national_code': ['exact'],
            'faculty': ['exact'],
            'major': ['exact'],
            'entry_year': ['exact'],
            'military_service_status': ['exact'],
        }


class EA_ModelFilter(django_filters.FilterSet):
    
    firstname = django_filters.CharFilter(field_name='assistant__firstname')
    lastname = django_filters.CharFilter(field_name='assistant__lastname')
    pr_number = django_filters.UUIDFilter(field_name='assistant__professor_number')
    national_code = django_filters.NumberFilter(field_name='assistant__national_code')
    
    faculty = django_filters.UUIDFilter(field_name='faculty__id')
    major = django_filters.UUIDFilter(field_name='assistant__major__id')
    
    
    class Meta:
        model = EducationalAssistant
        
        # see project document TODO
        fields = ['firstname', 
                  'lastname', 
                  'pr_number', 
                  'national_code', 
                  'faculty', 
                  'major']
        