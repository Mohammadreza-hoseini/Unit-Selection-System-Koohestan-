from django.urls import path
from term.Unit_selection.unit_views import URCreateView, URGetView, URGetStPk, SendFormSelection, AcceptOrRejectForm

urlpatterns = [
    path('student/<uuid:st_pk>/course_selection/create/', URCreateView.as_view(), name='create_UR'),
    path('student/course_selection/', URGetView.as_view(), name='get_allURDetails'),
    path('student/<uuid:st_pk>/course_selection/', URGetStPk.as_view(), name='get_StURDetails'),
    path('student/<uuid:st_pk>/course_selection/send-form/', SendFormSelection.as_view(), name='send_form_selection'),
    path('student/<uuid:st_pk>/accept_or_reject_form/<uuid:form_pk>/', AcceptOrRejectForm.as_view(),
         name='accept_or_reject_form'),
]
