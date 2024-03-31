from django.urls import path
from .views import StudentCreate, StudentGetUpdateDelete, EducationalAssistantView, EducationalAssistantWithPK, \
    GetAllStudents

app_name = 'accounts'
urlpatterns = [
    path('students/', StudentCreate.as_view(), name="students"),
    path('students_update/<uuid:pk>/', StudentGetUpdateDelete.as_view(), name="students_update"),
    path('students_get_all/', GetAllStudents.as_view(), name="students_get_all"),
    path(
        "assistants/", EducationalAssistantView.as_view(), name="educationalAssistant"
    ),
    path(
        "assistants/<uuid:pk>", EducationalAssistantWithPK.as_view(), name="EA_withPK"
    ),

]
