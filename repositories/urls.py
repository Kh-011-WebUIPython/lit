from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from repositories import views

urlpatterns = [
    url(r'^repositories/$', views.RepositoryList.as_view(), name='repository-list'),
    url(r'^repositories/(?P<pk>[0-9]+)$', views.RepositoryDetail.as_view(), name='repository-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
