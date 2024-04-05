from django.urls import path
from .views import TermView, GetAll_terms, TermWithPK

app_name = 'term'
urlpatterns = [
    path("create_term/", TermView.as_view(), name="create_term"),
    path("term_get_all/", GetAll_terms.as_view(), name="term_get_all"),
    path("termPK/<uuid:pk>", TermWithPK.as_view(), name='Term_withPK'),   
]