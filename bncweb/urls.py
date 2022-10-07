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
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth import views as password_views
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf import settings
# from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('game.urls')),
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('signout/', views.signout_view, name="signout"),
    path('reset_password/', password_views.PasswordResetView.as_view(
        template_name="reset_password.html"), name="reset_password"),
    path('password_reset_done/', password_views.PasswordResetDoneView.as_view(
        template_name="reset_password_done.html"), name="password_reset_done"),
    path('password_reset/<uidb64>/<token>/', password_views.PasswordResetConfirmView.as_view(
        template_name="reset_password_confirm.html"), name="password_reset_confirm"),
    path('password_reset_complete', password_views.PasswordResetCompleteView.as_view(
        template_name="reset_password_complete.html"), name="password_reset_complete"),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path('', include('game.urls')),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

