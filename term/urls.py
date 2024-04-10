from django.urls import include, path
from term.views import BusyStudyingRequestCreatGetUpdateDelete, UnitRegisterRequestGetData

app_name = 'term'

urlpatterns = [
    path('', include('term.Tr.tr_urls')),
    path('', include('term.Unit_selection.unit_urls')),
    path('student/<uuid:pk>/studying-evidence/', BusyStudyingRequestCreatGetUpdateDelete.as_view(),
         name='studying-evidence'),
    path('student/<uuid:pk>/class-schedule/', UnitRegisterRequestGetData.as_view(),
         name='studying-evidence'),

]
