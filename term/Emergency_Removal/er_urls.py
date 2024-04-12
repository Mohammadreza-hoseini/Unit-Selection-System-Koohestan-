from django.urls import path
from .er_views import StudentEmergencyRemoval, AssistantAcceptOrRejectEmergencyRemoval

urlpatterns = [
    path('student/<uuid:student_id>/courses/<uuid:course_id>/emergency-remove/', StudentEmergencyRemoval.as_view(),
         name='student_emergency_removal'),
    path('assistant/<uuid:assistant_id>/emergency-remove/<uuid:emergency_removal_id>/',
         AssistantAcceptOrRejectEmergencyRemoval.as_view(),
         name='assistant_emergency_removal')
]
