from django.urls import path
from .tr_views import TermView, GetAll_terms, TermWithPK

urlpatterns = [
    path("create_term/", TermView.as_view(), name="terms_create"),
    path("term_pk/<uuid:pk>", TermWithPK.as_view(), name='terms_pk'),   
    path("term_get_all/", GetAll_terms.as_view(), name="terms_get_all"),
]