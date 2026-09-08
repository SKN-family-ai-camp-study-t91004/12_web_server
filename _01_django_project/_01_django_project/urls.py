"""

- 현재 프로젝트(서버)의 URL 입구
- 경로 앞부분으로 앱을 선택하고 나머지는 앱 별로 존재하는 urls.py로 넘긴다

URL configuration for _01_django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirect: 재요청
    path('', RedirectView.as_view(url='first/')),

    # 요청 주소에서 앞부분 'frist/'를 제외한 부분을
    # 'first.urls'로 전달
    path('first/', include('first.urls')),

    path('second/', include('second.urls')),
]
