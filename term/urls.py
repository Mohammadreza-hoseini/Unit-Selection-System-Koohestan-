from django.urls import include, path

app_name = 'term'

urlpatterns = [
    path('', include('term.Tr.tr_urls')),
    path('', include('term.Unit_selection.unit_urls')),
]