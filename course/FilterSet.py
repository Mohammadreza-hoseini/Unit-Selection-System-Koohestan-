import django_filters
from .models import Course


#TODO:

class CourseModelFilter(django_filters.FilterSet):
    class Meta:
        #TODO
        model = Course
        fields = "__all__"
