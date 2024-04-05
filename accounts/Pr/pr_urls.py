from django.urls import path

from accounts.Pr.pr_views import ProfessorCreate, ProfessorGetUpdateDelete,GetAllProfessors

urlpatterns = [
    path('professors_create/', ProfessorCreate.as_view(), name="professors_create"),
    path('professors_pk/<uuid:pk>', ProfessorGetUpdateDelete.as_view(), name="professors_pk"),
    path('professors_get_all/', GetAllProfessors.as_view(), name="professors_get_all"),
]
