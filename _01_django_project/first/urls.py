from django.urls import path
from . import views

app_name = 'first'
urlpatterns = [
    path('', views.index, name='index'),
    path('greeting/', views.greeting, name='greeting'),
    path('foo/', views.foo, name='foo'),
    path('bar/', views.bar, name='bar'),
]