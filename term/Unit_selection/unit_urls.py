from django.urls import path

from term.Unit_selection.unit_views import URCreateView, URGetView

urlpatterns = [
    path('student/<uuid:st_pk>/course_selection/create/', URCreateView.as_view(), name='create_courseSelectionForm'),
    path('student/<uuid:st_pk>/course_selection/', URGetView.as_view(), name='get_courseSelectionDetails'),
]
