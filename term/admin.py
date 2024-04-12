from django.contrib import admin
from .models import Term, UnitRegisterRequest, BusyStudyingRequest, EmergencyRemoval

# Register your models here.
admin.site.register(Term)
admin.site.register(UnitRegisterRequest)
admin.site.register(BusyStudyingRequest)
admin.site.register(EmergencyRemoval)
