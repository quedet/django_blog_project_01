from django.urls import path
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetView, PasswordResetDoneView, 
                                       PasswordResetConfirmView, PasswordResetCompleteView)

from accounts.forms import UserLoginForm, UserPasswordResetForm

from accounts.views import user_registration, edit_profile, user_dashboard, UserProfileView, PostCreateView, PostUpdateView, PostDeleteView

app_name = 'accounts'

urlpatterns = [
    # Login and Logout
    path('login/', LoginView.as_view(template_name='accounts/registration/login.html', form_class=UserLoginForm), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('signup/', user_registration, name='user_signup'),
    #
    path('profile/edit/', edit_profile, name='user_edit_profile'),
    path('profile/me/', UserProfileView.as_view(), name='user_profile'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    
    # Manage Posts
    path('profile/posts/create/', PostCreateView.as_view(), name='user_profile_post_create'),
    path('profile/posts/<pk>/edit/', PostUpdateView.as_view(), name='user_profile_post_update'),
    path('profile/posts/<pk>/delete/', PostDeleteView.as_view(), name='user_profile_post_delete'),
    
    # Reset Password Functionalities
    path('password_reset/', PasswordResetView.as_view(template_name='accounts/registration/password_reset_form.html', 
                                                      email_template_name='accounts/registration/password_reset_email.html', 
                                                      success_url='/accounts/password_reset/done/', 
                                                      form_class=UserPasswordResetForm), name='user_password_reset'),
    
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='accounts/registration/password_reset_done.html'), 
                                                        name='user_password_reset_done'),
    
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/registration/password_reset_confirm.html', 
                                                                     success_url='/accounts/reset/done/'),
                                                                        name='user_password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='accounts/registration/password_reset_complete.html'
                                                          ), name='user_password_reset_complete')
]