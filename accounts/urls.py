from django.urls import path
from .views import StudentCreate, EducationalAssistantView

app_name = "accounts"
urlpatterns = [
    path("students/", StudentCreate.as_view(), name="students"),
    path(
        "assistants/", EducationalAssistantView.as_view(), name="educationalAssistant"
    ),
]
