from django.urls import path

from . import views

app_name = 'conversation'

app_name = 'conversation'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.detail, name='detail'),
    path('eliminar/<int:message_id>/', views.eliminar_mensaje, name='eliminar_mensaje'),
    path('new/<int:item_pk>/', views.new_conversation, name='new'),
]