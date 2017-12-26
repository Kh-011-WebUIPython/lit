from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from branches import views

urlpatterns = [
    url(r'^repositories/(?P<repository_id>[0-9]+)/branches/$', views.BranchList.as_view(), name='branch-list'),
    url(r'^repositories/(?P<repository_id>[0-9]+)/branches/(?P<branch_id>[0-9]+)/$', views.BranchDetail.as_view(), name='branch-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)