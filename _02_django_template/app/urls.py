from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        '01_variables_filters',
        views.variables_filters,
        name='01_variables_filters',
    ),
    path('02_tags', views.tags, name='02_tags'),
    path('03_layout', views.layout, name='03_layout'),
    path('04_staticfiles', views.staticfiles, name='04_staticfiles'),
    path('05_urls', views.urls, name='05_urls'),

    # <int:id> : 전달 받은 값을 int로 형변환해서 id 매개변수에 전달
    path('article/<int:id>', views.article, name='article'),

    path('search', views.search, name='search'),

    path('06_bootstrap', views.bootstrap, name='06_bootstrap'),
]