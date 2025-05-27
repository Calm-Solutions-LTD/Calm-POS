from django.urls import path
from . import api, views

# views
urlpatterns = [
    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('forgot-password/', views.forgot_password_page, name='forgot_password_page'),
    path('reset-password/', views.reset_password_page, name='reset_password_page'),
    path('logout/', views.logout_view, name='logout'),
]

# api
urlpatterns += [
    path('api/register/', api.register, name='api_register'),
    path('api/login/', api.login, name='api_login'),
    path('api/forgot-password/', api.forgot_password, name='api_forgot_password'),
    path('api/reset-password/', api.reset_password, name='api_reset_password'),
    path('api/send-2fa-code/', api.send_2fa_code, name='api_send_2fa_code'),
    path('api/verify-2fa/', api.verify_2fa, name='api_verify_2fa'),
    path('api/logout/', api.logout_api, name='api_logout'),
]