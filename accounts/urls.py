from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordChangeDoneView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)
from accounts.views import SignUpView
from accounts.forms import EmailAuthenticationForm

from django.urls import path


signup_view = SignUpView.as_view()
login_view = LoginView.as_view(
    form_class=EmailAuthenticationForm,
    redirect_authenticated_user=True,
    template_name='accounts/login.html'
)
logout_view = LogoutView.as_view()
password_change_view = PasswordChangeView.as_view()
password_change_done_view = PasswordChangeDoneView.as_view()
password_reset_view = PasswordResetView.as_view()
password_reset_done_view = PasswordResetView.as_view()
password_reset_confirm_view = PasswordResetConfirmView.as_view()
password_reset_complete_view = PasswordResetCompleteView.as_view()

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_change/', password_change_view, name='password_change'),
    path('password_change/done/', password_change_done_view, name='password_change_done'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset/done/', password_reset_done_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/done/', password_reset_complete_view, name='password_reset_complete'),
]