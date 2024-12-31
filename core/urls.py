from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_auth')),
    path('usuarios/', include('users.urls')),
    path('viaticos/', include('perdiems.urls')),
    path('login/',    include('authentication.urls')),
    path('',          include('home.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path("general/",  include('general.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
