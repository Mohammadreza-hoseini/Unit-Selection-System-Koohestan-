from django.urls import path
from .views import StudentCreate, StudentGetUpdateDelete, EducationalAssistantView, EducationalAssistantWithPK, \
    GetAllStudents, GetAll_EAs
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'accounts'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('students/', StudentCreate.as_view(), name="students"),
    path('students_update/<uuid:pk>/', StudentGetUpdateDelete.as_view(), name="students_update"),
    path('students_get_all/', GetAllStudents.as_view(), name="students_get_all"),
    path(
        "assistants/", EducationalAssistantView.as_view(), name="educationalAssistant"
    ),
    path('assistants_get_all/', GetAll_EAs.as_view(), name="assistants_get_all"),
    path(
        "assistants/<uuid:pk>", EducationalAssistantWithPK.as_view(), name="EA_withPK"
    )
]
