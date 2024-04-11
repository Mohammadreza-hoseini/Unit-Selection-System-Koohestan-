from django.urls import path

from course.appeal_requests.ApReq_views import ScoreTableView

urlpatterns = [
    
    # just for test #TODO
    path('prof/score/', ScoreTableView.as_view(), name='add_score'),
]