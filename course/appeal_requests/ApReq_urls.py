from django.urls import path

from course.appeal_requests.ApReq_views import ScoreTableView, ApReqView

urlpatterns = [
    path('prof/score/<uuid:pr_pk>/<uuid:course_pk>', ScoreTableView.as_view(), name='add_score'),
    path('student/<uuid:st_pk>/appeal_request/<uuid:course_pk>', ApReqView.as_view(), name='apply_req')
]