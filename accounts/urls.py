from django.urls import path
from .views import StudentGetCreate, StudentGetUpdateDelete, EducationalAssistantView, EducationalAssistantWithPK

app_name = 'accounts'
urlpatterns = [
    path('students/', StudentGetCreate.as_view(), name="students"),
    path('students_update/<uuid:pk>/', StudentGetUpdateDelete.as_view(), name="students_update"),
    path(
        "assistants/", EducationalAssistantView.as_view(), name="educationalAssistant"
    ),
    path(
        "assistants/<uuid:pk>", EducationalAssistantWithPK.as_view(), name="EA_withPK"
    ),
    
]
