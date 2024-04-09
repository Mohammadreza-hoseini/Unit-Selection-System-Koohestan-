from django.urls import include, path

from term.views import busystudyingrequestCreatGetUpdateDelete

app_name = 'term'

urlpatterns = [
    path('/student/<uuid:pk>/studying-evidence/', busystudyingrequestCreatGetUpdateDelete.as_view(), name='studying-evidence')
]