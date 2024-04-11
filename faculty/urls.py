from django.urls import path
from .views import FacultyGetUpdateDelete, FacultyCreate, GetAllFaculty

app_name = 'faculty'
urlpatterns = [
    path('faculties/', GetAllFaculty.as_view(), name='list_faculties'),
    path('create/', FacultyCreate.as_view(), name='create_faculty'),
    path('faculty_update/<uuid:pk>/', FacultyGetUpdateDelete.as_view(), name='faculty_with_uuid'),

]
