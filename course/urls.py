from django.urls import path
from .views import CourseView, GetAll_courses, CourseWithPK, SubjectCreate, GetAllSubjects, SubjectGetUpdateDelete

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'courses'
urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        "subject_create/", SubjectCreate.as_view(), name="subject_create"
    ),
    path(
        "courses/", CourseView.as_view(), name="course_create"
    ),
    path("subjects/", GetAllSubjects.as_view(), name="subject_get_all"),
    path("subjects/<uuid:pk>/", SubjectGetUpdateDelete.as_view(), name="subject_create"),
    path('courses_get_all/', GetAll_courses.as_view(), name="courses_get_all"),
    path(
        "courses/<uuid:pk>", CourseWithPK.as_view(), name="course_withPK"
    )
]
