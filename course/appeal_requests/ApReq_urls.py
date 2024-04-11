from django.urls import path

from course.appeal_requests.ApReq_views import ScoreTableView

urlpatterns = [
    
    # just for test #TODO
    path('prof/score/<uuid:pr_pk>/<uuid:course_pk>', ScoreTableView.as_view(), name='add_score'),
]