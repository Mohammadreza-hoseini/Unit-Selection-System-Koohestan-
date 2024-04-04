import django_filters
from .models import Course, Subject


# TODO:

class CourseModelFilter(django_filters.FilterSet):
    class Meta:
        # TODO
        model = Course
        fields = "__all__"


class SubjectModelFilter(django_filters.FilterSet):
    class Meta:
        model = Subject
        fields = {
            'name': ['exact'],
            'provider_faculty': ['exact'],
        }
