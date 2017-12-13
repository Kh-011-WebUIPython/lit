from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from branches import views

urlpatterns = [
    url(r'^branches/$', views.BranchList.as_view(), name='branch-list'),
    url(r'^branches/(?P<pk>[0-9]+)/$', views.BranchDetail.as_view(), name='branch-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)