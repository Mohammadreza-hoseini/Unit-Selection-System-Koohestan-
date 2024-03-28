from django.urls import path
from .views import StudentGetCreate, StudentGetUpdateDelete

app_name = 'accounts'
urlpatterns = [
    path('students/', StudentGetCreate.as_view(), name="students"),
    path('students_update/<uuid:pk>/', StudentGetUpdateDelete.as_view(), name="students_update"),
]
