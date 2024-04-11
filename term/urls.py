from django.urls import include, path
from term.views import BusyStudyingRequestCreatGetUpdateDelete, UnitRegisterRequestGetData, \
    BusyStudyingRequestAcceptOrReject, EducationalAssistantGetAllBusyStudyingRequest

app_name = 'term'

urlpatterns = [
    path('', include('term.Tr.tr_urls')),
    path('', include('term.Unit_selection.unit_urls')),
    path('student/<uuid:pk>/studying-evidence/', BusyStudyingRequestCreatGetUpdateDelete.as_view(),
         name='studying-evidence'),
    path('student/<uuid:pk>/class-schedule/', UnitRegisterRequestGetData.as_view(),
         name='studying-evidence'),
    path('assistant/<uuid:assistant_id>/accept_or_reject/<uuid:studying_id>/',
         BusyStudyingRequestAcceptOrReject.as_view(),
         name='accept_or_reject'),
    path('assistant/<uuid:assistant_id>/get_all_busy_studying_requests/',
         EducationalAssistantGetAllBusyStudyingRequest.as_view(), name='get_all_busy_studying_requests'),
]
