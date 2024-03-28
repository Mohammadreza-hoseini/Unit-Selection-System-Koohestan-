from django.urls import path
from .views import ProfessorCreateView

app_name = 'account'

urlpatterns = [
    path('professor/create/', ProfessorCreateView.as_view(), name='createProfessor'),
]