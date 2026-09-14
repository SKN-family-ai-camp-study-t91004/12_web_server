from django.urls import path
from . import views, views_stream, views_ollama

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('init_chat', views.init_chat, name='init_chat'),
    path('chat', views.chat, name='chat'),
    path('del_chat', views.del_chat, name='del_chat'),

    path('stream/', views_stream.stream_index, name='stream_index'),
    path('chat_stream', views_stream.chat_stream, name='chat_stream'),

    path('ollama/', views_ollama.ollama_index, name='ollama_index'),
    path('chat_ollama', views_ollama.chat_ollama, name='chat_ollama'),
]
