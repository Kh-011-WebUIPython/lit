from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from repositories import views

urlpatterns = [
    url(r'^repositories/$', views.RepositoryList.as_view(), name='repository-list'),
    url(r'^repositories/(?P<repository_id>[0-9]+)$', views.RepositoryDetail.as_view(), name='repository-detail'),
    url(r'^repositories/(?P<repository_id>[0-9]+)/push_check_commits/$', views.push_check_commits, name='repository-push-check-commits'),
    url(r'^repositories/(?P<repository_id>[0-9]+)/push_add_commits/$', views.push_add_commits,
        name='repository-push-add-commits')

]

urlpatterns = format_suffix_patterns(urlpatterns)
