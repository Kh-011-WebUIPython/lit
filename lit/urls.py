from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

import lit
from lit.settings.base import DEBUG
from .views import api_root

urlpatterns = [
                  url(r'^$', api_root),
                  url(r'^docs/', include_docs_urls(title='Todo API', description='RESTful API for Todo')),
                  url(r'^admin/', admin.site.urls),
                  url(r'^auth/', obtain_jwt_token),
                  url(r'^auth-refresh/', refresh_jwt_token),
                  url(r'^auth-verify/', verify_jwt_token),
                  url(r'^', include('users.urls', namespace='users')),
                  url(r'^', include('repositories.urls', namespace='repositories')),
                  url(r'^', include('permissions.urls', namespace='permissions')),
                  url(r'^', include('branches.urls', namespace='branches')),
                  url(r'^', include('commits.urls', namespace='commits')),
              ] + static(lit.settings.base.MEDIA_URL, document_root=lit.settings.base.MEDIA_ROOT)

if DEBUG:
    import debug_toolbar

    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
