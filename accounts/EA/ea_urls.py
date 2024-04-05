from django.urls import path
from accounts.EA.ea_views import EducationalAssistantView, EducationalAssistantWithPK, GetAll_EAs

urlpatterns = [
    path("EA_create/", EducationalAssistantView.as_view(), name="EA_create"),
    path('EA_get_all/', GetAll_EAs.as_view(), name="EA_get_all"),
    path("EA_pk/<uuid:pk>", EducationalAssistantWithPK.as_view(), name="EA_pk")
]
