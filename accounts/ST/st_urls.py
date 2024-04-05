from django.urls import path

from .st_views import StudentPassedCourses_PK, StudentCreate, StudentGetUpdateDelete, GetAllStudents

urlpatterns = [
    path("StudentPassedCourses_PK/", StudentPassedCourses_PK.as_view(), name="StudentPassedCourses_PK"),  
    path('students_create/', StudentCreate.as_view(), name="students_create"),
    path('students_pk/<uuid:pk>/', StudentGetUpdateDelete.as_view(), name="students_pk"),
    path('students_get_all/', GetAllStudents.as_view(), name="students_get_all"),
]
