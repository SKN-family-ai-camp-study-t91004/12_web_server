from django.contrib import auth
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from .forms import UserForm
from .models import UserDetail


@require_POST
def logout(request):
    # 로그아웃도 세션을 변경하므로 CSRF 검증을 거친 POST만 허용한다.
    auth.logout(request)
    return redirect('qna:index')


@require_http_methods(['GET', 'POST'])
def signup(request):
    # GET의 None은 빈 폼, POST와 FILES는 검증할 텍스트·파일을 뜻한다.
    # 파일은 POST 딕셔너리에 없으므로 multipart 폼과 두 번째 인수가 함께 필요하다.
    form = UserForm(request.POST if request.method == 'POST' else None,
                    request.FILES if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        # 두 DB 행은 함께 성공하거나 함께 롤백한다. 업로드 파일 저장은 DB 트랜잭션 밖이다.
        with transaction.atomic():
            user = form.save()
            UserDetail.objects.create(user=user, birthday=form.cleaned_data['birthday'], profile=form.cleaned_data['profile'])
        # 검증된 비밀번호·cleaned_data 전체를 로그로 출력하지 않는다.
        # 저장된 User를 세션에 연결한다. 다음 요청에서 request.user로 복원된다.
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('qna:index')
    return render(request, 'uauth/signup.html', {'form': form})


@require_GET
def check_username(request):
    # 이 JSON은 입력 중 안내용이다. 가입 순간의 중복 여부는 UserForm이 다시 검사한다.
    username = request.GET.get('username', '').strip()
    return JsonResponse({'available': len(username) >= 4 and not User.objects.filter(username=username).exists()})
