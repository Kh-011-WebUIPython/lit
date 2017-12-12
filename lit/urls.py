from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

from .views import api_root

urlpatterns = [
    url(r'^$', api_root),
    url(r'^docs/', include_docs_urls(title='Todo API', description='RESTful API for Todo')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('users.urls', namespace='users')),
    url(r'^', include('repositories.urls', namespace='repositories')),
]
