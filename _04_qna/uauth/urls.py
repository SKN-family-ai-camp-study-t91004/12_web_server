from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'uauth'

urlpatterns = [
    # as_view()가 클래스의 요청 처리를 URL에서 호출 가능한 View로 연결한다.
    # GET은 폼, POST는 AuthenticationForm 검증 후 로그인 세션을 만든다.
    path('login/', auth_views.LoginView.as_view(template_name='uauth/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('signup/', views.signup, name='signup'),

    path('check_username/', views.check_username, name='check_username'),
]
