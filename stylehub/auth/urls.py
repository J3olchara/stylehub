"""urls for auth app"""
import django.contrib.auth.views as default_views
import django.urls

import auth.forms as auth_forms
import auth.views as auth_views

app_name = 'auth'

urlpatterns = [
    django.urls.path(
        'login/',
        auth_views.CustomLoginView.as_view(),
        name='login',
    ),
    django.urls.path(
        'logout/',
        default_views.LogoutView.as_view(
            template_name='home/index.html',
        ),
        name='logout',
    ),
    django.urls.path(
        'password_change/',
        default_views.PasswordChangeView.as_view(
            template_name='auth/password_change.html',
            form_class=auth_forms.PasswordChangeForm,
        ),
        name='password_change',
    ),
    django.urls.path(
        'password_change/done/',
        auth_views.CustomChangePasswordDone.as_view(),
        name='password_change_done',
    ),
    django.urls.path(
        'password_reset/',
        default_views.PasswordResetView.as_view(
            template_name='auth/password_reset.html',
            form_class=auth_forms.PasswordResetForm,
        ),
        name='password_reset',
    ),
    django.urls.path(
        'password_reset/done/',
        auth_views.CustomPasswordResetDone.as_view(),
        name='password_reset_done',
    ),
    django.urls.path(
        'reset/<uidb64>/<token>/',
        default_views.PasswordResetConfirmView.as_view(
            template_name='auth/password_change.html',
            form_class=auth_forms.PasswordResetConfirmForm,
        ),
        name='password_reset_confirm',
    ),
    django.urls.path(
        'reset/done/',
        auth_views.CustomPasswordResetComplete.as_view(),
        name='password_reset_complete',
    ),
    django.urls.path(
        'signup/',
        auth_views.SignUp.as_view(),
        name='signup',
    ),
    django.urls.path(
        'signup/done/', auth_views.SignUpDone.as_view(), name='signup_done'
    ),
    django.urls.path(
        'signup/<int:user_id>/<uuid:token>/',
        auth_views.SignUpConfirm.as_view(),
        name='signup_confirm',
    ),
]
