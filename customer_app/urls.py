from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('save_domain', views.save_domain, name='save_domain'),
    path('user_domains/', views.user_domains, name='user_domains'),
    path('refresh_domain/<int:domain_id>/', views.refresh_domain, name='refresh_domain'),
    path('delete-domain/<int:domain_id>/', views.delete_domain, name='delete_domain'),
    path('profile', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('doamin_details/<int:domain_id>/', views.doamin_details, name='doamin_details'),
    path('settings/', views.settings, name='settings'),
    path('notification/', views.notification, name='notification'),
    path('send_mail/', views.send_mail, name='send_mail'),
    path('check_expiring/', views.check_expiring, name='check_expiring'),
]