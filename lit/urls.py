from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.documentation import include_docs_urls


from lit.views import api_root
from lit.settings.base import DEBUG, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
                  url(r'^$', api_root),
                  url(r'^api/v1/docs/', include_docs_urls(title='LIT API', description='REST API for LIT')),
                  url(r'^administrator/', admin.site.urls),
                  url(r'^api/v1/auth/', include('rest_auth.urls')),
                  url(r'^api/v1/', include('users.urls', namespace='users')),
                  url(r'^api/v1/', include('repositories.urls', namespace='repositories')),
                  url(r'^api/v1/', include('permissions.urls', namespace='permissions')),
                  url(r'^api/v1/', include('branches.urls', namespace='branches')),
                  url(r'^api/v1/', include('commits.urls', namespace='commits')),
              ] + static(MEDIA_URL, document_root=MEDIA_ROOT)

if DEBUG:
    import debug_toolbar

    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
