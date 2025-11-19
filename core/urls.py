from django.urls import path
from django.contrib.auth import views as auth_views
from .views_auth import CustomPasswordResetView,CustomPasswordResetCompleteView,CustomPasswordResetConfirmView
from . import views
from .forms import LoginForm

app_name = 'core'  # Esto define el namespace 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),  
    
    path('send_email/', views.enviar_correo, name='send_email'),
    
    # Notificaciones
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification_view, name='delete_notification'),
    path('api/notifications/count/', views.get_notifications_count, name='notifications_count'),
]