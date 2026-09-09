from django.urls import path
from . import views

app_name = 'qna'

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:id>', views.question_detail, name='question_detail'),
    path('question/create/', views.question_create, name='question_create'),
]