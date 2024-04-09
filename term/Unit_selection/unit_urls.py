from django.urls import path

from term.Unit_selection.unit_views import URCreateView, URGetView, URGetStPk

urlpatterns = [
    path('student/<uuid:st_pk>/course_selection/create/', URCreateView.as_view(), name='create_UR'),
    path('student/course_selection/', URGetView.as_view(), name='get_allURDetails'),
    path('student/<uuid:st_pk>/course_selection/', URGetStPk.as_view(), name='get_StURDetails'),
]
