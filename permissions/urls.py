from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from permissions import views

urlpatterns = [
    url(r'^permissions/$', views.PermissionList.as_view(), name='permission-list'),
    url(r'^permissions/(?P<pk>[0-9]+)$', views.PermissionDetail.as_view(), name='permission-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
