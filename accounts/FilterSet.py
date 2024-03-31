import django_filters
from .models import Student


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
