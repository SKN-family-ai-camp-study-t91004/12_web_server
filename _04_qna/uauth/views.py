from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from .forms import ProfileForm, UserForm
from .models import UserDetail

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


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

        # 별도의 트랜잭션을 새롭게 생성하여, 내부에서 오류가 발생하지 않으면 commit
        # 오류가 발생하면 rollback
        with transaction.atomic():
            user = form.save()
            UserDetail.objects.create(user=user, birthday=form.cleaned_data['birthday'],
                                      profile=form.cleaned_data['profile'])
        # 검증된 비밀번호·cleaned_data 전체를 로그로 출력하지 않는다.
        # 저장된 User를 세션에 연결한다. 다음 요청에서 request.user로 복원된다.
        # 회원 가입 성공 시 로그인
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('qna:index')
    return render(request, 'uauth/signup.html', {'form': form})


@require_GET
def check_username(request):
    # 이 JSON은 입력 중 안내용이다. 가입 순간의 중복 여부는 UserForm이 다시 검사한다.
    username = request.GET.get('username', '').strip()
    return JsonResponse({'available': len(username) >= 4 and not User.objects.filter(username=username).exists()})


@login_required(login_url='uauth:login')
@require_http_methods(['GET', 'POST'])
def password_change(request):
    # 현재 비밀번호와 새 비밀번호 두 입력의 검증을 Django 기본 폼에 맡긴다.
    form = PasswordChangeForm(request.user, request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()  # 이미 존재하는 user의 비밀번호를 update
        # 변경된 비밀번호 해시를 현재 세션에도 반영해 이 브라우저의 로그인을 유지한다.
        auth.update_session_auth_hash(request, user)

        messages.success(request, '비밀번호를 변경했습니다.')
        return redirect('qna:index')
    return render(request, 'uauth/password_change.html', {'form': form})


@login_required(login_url='uauth:login')
@require_http_methods(['GET', 'POST'])
def profile_edit(request):
    # URL이나 폼의 사용자 번호를 받지 않고 로그인한 본인의 프로필만 조회한다.
    detail = UserDetail.objects.filter(user=request.user).first()
    if detail is None:
        detail = UserDetail(user=request.user)  # GET에서는 저장하지 않고 POST 검증 성공 시 생성한다.
    form = ProfileForm(request.POST if request.method == 'POST' else None,
                       request.FILES if request.method == 'POST' else None,
                       instance=detail)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '프로필을 수정했습니다.')
        return redirect('qna:index')
    return render(request, 'uauth/profile_edit.html', {'form': form})
