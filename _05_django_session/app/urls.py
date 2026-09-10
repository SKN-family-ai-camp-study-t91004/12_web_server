from django.urls import path

from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('set_session/', views.set_session, name='set_session'),
    path('clear_session/', views.clear_session, name='clear_session'),
]