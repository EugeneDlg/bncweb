from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth import views as password_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('reset_password/', password_views.PasswordResetView.as_view(
        template_name="reset_password.html", email_template_name="password_reset_email.html"), name="reset_password"),
    path('password_reset_done/', password_views.PasswordResetDoneView.as_view(
        template_name="reset_password_done.html"), name="password_reset_done"),
    path('password_reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(
        template_name="reset_password_confirm.html"), name="password_reset_confirm"),
    path('password_reset_complete', password_views.PasswordResetCompleteView.as_view(
        template_name="reset_password_complete.html"), name="password_reset_complete"),
    path('edit/', views.edit_profile, name="edit"),
    path('changepassword/', views.changepassword, name="changepassword"),
    path('delete/', views.delete_profile, name="delete"),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)