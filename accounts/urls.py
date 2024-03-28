from django.urls import path
from .views import StudentCreate

app_name = 'accounts'
urlpatterns = [
    path('students/', StudentCreate.as_view(), name="students"),
]
