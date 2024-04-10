from django.urls import include, path

from term.views import BusyStudyingRequestCreatGetUpdateDelete

app_name = 'term'

urlpatterns = [
    path('student/<uuid:pk>/studying-evidence/', BusyStudyingRequestCreatGetUpdateDelete.as_view(),
         name='studying-evidence'),
    path('', include('term.Unit_selection.unit_urls')),
    path('', include('term.Tr.tr_urls')),
]
