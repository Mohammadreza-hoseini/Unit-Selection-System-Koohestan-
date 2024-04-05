from django.urls import path

from accounts.ST.st_views import StudentPassedCourses_PK

urlpatterns = [
    path("StudentPassedCourses_PK/", StudentPassedCourses_PK.as_view(), name="StudentPassedCourses_PK"),  
]
