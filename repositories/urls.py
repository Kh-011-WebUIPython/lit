from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from repositories import views

urlpatterns = [
    url(r'^repositories/$', views.RepositoryList.as_view(), name='repository-list'),
    url(r'^repositories/(?P<repository_id>[0-9]+)$', views.RepositoryDetail.as_view(), name='repository-detail'),
    url(r'^repositories/(?P<repository_id>[0-9]+)/push/$', views.RepositoryDetail.as_view(), name='repository-push')
]

urlpatterns = format_suffix_patterns(urlpatterns)
