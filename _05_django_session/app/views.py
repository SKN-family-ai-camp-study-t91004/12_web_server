"""폼 입력 → DB 세션 저장 → 다음 GET에서 복원하는 흐름을 다룬다."""
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST


def index(request):
    # 읽기만 하는 GET은 만료 시간을 연장하지 않는다. 저장 시점부터 60초 후 만료한다.
    return render(request, 'app/index.html')


@require_POST
def set_session(request):

    # 사용자가 POST 방식 요청 시 같이 제출한 값 중 'username' 얻어오기
    # == <input name='username'> 에 작성해서 제출한 값
    # - 제출이 안된 경우 기본 값으로 ''(빈칸)
    # - 양쪽 공백 제거
    username = request.POST.get('username', '').strip()
    if not username or len(username) > 40:

        # HTTP 응답 상태 코드 400(BadRequest)을 반환해라
        return HttpResponseBadRequest('이름은 1~40자로 입력한다.')
    # 기본 JSON serializer가 지원하는 문자열·숫자·bool·list·dict만 저장한다.
    # datetime 객체는 직접 저장하지 않고 날짜 문자열로 변환한다.
    # 기본 DB 세션은 이 값을 서버의 django_session에 저장하고, 브라우저에는 세션 키만 쿠키로 보낸다.
    request.session.update({
        'username': username,
        'point': 1234567890,
        'prob': 12345.67890,
        'expired': True,  # bool 표시용 모의값이며 실제 세션 만료 여부와 무관하다.
        'nums': [1, 2, 3, 4, 5],
        'data': {'message': '안녕~ 세션 🎱🎱🎱', 'today': timezone.localdate().isoformat()},
    })
    request.session.set_expiry(60)  # 이 쓰기 요청에서만 만료 시각을 갱신한다.
    return redirect('app:index')


# session을 강제로 만료(무효화)시키는 요청은 POST만 가능!
@require_POST
def clear_session(request):
    # 값과 세션 키를 함께 폐기한다. GET으로는 삭제할 수 없으며 CSRF 검사도 적용한다.
    request.session.flush()
    return redirect('app:index')