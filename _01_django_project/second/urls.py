from django.urls import path
from . import views

app_name = 'second'
urlpatterns = [
    path('', views.index, name='index'),
    path('hello/', views.hello, name='hello')
]

# startapp 수행 후 해야할 일
# 1) settings.py > INSTALLED_APPS에 앱 등록
# 2) 설정폴더/urls.py > urlpatterns 등록
# 3) 생성한 앱 폴더/urls.py 생성