from django.urls import path, include
from .views import StudentCreate, StudentGetUpdateDelete, EducationalAssistantView, EducationalAssistantWithPK, \
    GetAllStudents, GetAll_EAs, RequestOTPView, ChangePassword, ProfessorCreate, ProfessorGetUpdateDelete,GetAllProfessors
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'accounts'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('professor/', ProfessorCreate.as_view(), name="professor"),
    path('professor_update/<uuid:pk>/', ProfessorGetUpdateDelete.as_view(), name="professor_update"),
    path('professor_get_all/', GetAllProfessors.as_view(), name="professor_get_all"),
    path('change_password_request/', RequestOTPView.as_view(), name="change_password_request"),
    path('change_password_action/', ChangePassword.as_view(), name="change_password_action"),
    path(
        "assistants/", EducationalAssistantView.as_view(), name="educationalAssistant"
    ),
    path('assistants_get_all/', GetAll_EAs.as_view(), name="assistants_get_all"),
    path(
        "assistants/<uuid:pk>", EducationalAssistantWithPK.as_view(), name="EA_withPK"
    ),
    path('', include('accounts.ST.st_urls')),
]