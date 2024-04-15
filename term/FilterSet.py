import django_filters
from .models import Term


#TODO:

class TermModelFilter(django_filters.FilterSet):
    class Meta:
        model = Term
        fields = ["name", ]
