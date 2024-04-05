import django_filters
from .models import Course, Subject


class CourseModelFilter(django_filters.FilterSet):
    
    subject_name = django_filters.CharFilter(field_name='subject__name')
    faculty_name = django_filters.CharFilter(field_name="subject__provider_faculty__name")
    term = django_filters.CharFilter(field_name='term__name')
    
    class Meta:
        model = Course
        fields = ['subject_name', 'faculty_name', 'term']


class SubjectModelFilter(django_filters.FilterSet):
    class Meta:
        model = Subject
        fields = {
            'name': ['exact'],
            'provider_faculty': ['exact'],
        }
