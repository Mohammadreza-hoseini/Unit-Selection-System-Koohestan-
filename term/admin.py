from django.contrib import admin
from .models import Term, UnitRegisterRequest, BusyStudyingRequest

# Register your models here.
admin.site.register(Term)
admin.site.register(UnitRegisterRequest)
admin.site.register(BusyStudyingRequest)
