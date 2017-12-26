from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from commits import views

urlpatterns = [
    url(r'^repositories/(?P<repository_id>[0-9]+)/branches/(?P<branch_id>[0-9]+)/commits/$', views.CommitList.as_view(),
        name='commit-list'),
    url(r'^repositories/(?P<repository_id>[0-9]+)/branches/(?P<branch_id>[0-9]+)/commits/(?P<commit_id>[0-9]+)$',
        views.CommitDetail.as_view(), name='commit-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
