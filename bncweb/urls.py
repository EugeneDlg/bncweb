"""bncweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth import views as password_views
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
# from django.conf.urls import url

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('game.urls')), # может удалить
    path('login/', views.login_view, name="login"),
    path('', include('game.urls')),
    path('', include('users.urls')),
    # path('api/users/', views.GetUsers.as_view()),
]

schema_view = get_schema_view(
    openapi.Info(
        title="BnC REST API",
        default_version='v1.0',
        description="API for BnC Game",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

router = routers.SimpleRouter()
router.register('users', views.UsersViewSet, basename='users')

urlpatterns += [
    path('api/', include(router.urls)),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

