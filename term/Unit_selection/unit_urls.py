from django.urls import path

from term.Unit_selection.unit_views import UR_CreateView, UR_GetView

urlpatterns = [
    path('student/<uuid:st_pk>/course_selection/create/', UR_CreateView.as_view(), name='create_courseSelectionForm'),
    path('student/<uuid:st_pk>/course_selection/', UR_GetView.as_view(), name='get_courseSelectionDetails'),
]