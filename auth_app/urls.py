from django.urls import path
from .views import customer_signup, customer_signin, logout_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('customer_signup', customer_signup, name='customer_signup'),
    path('customer_signin', customer_signin, name='customer_signin'),
    path('logout/', logout_view, name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='auth_app/password_change.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='auth_app/password_change_done.html'), name='password_change_done')
]