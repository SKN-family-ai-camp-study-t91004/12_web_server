"""OpenAI 호환 Ollama 서버를 사용하는 별도 스트리밍 화면과 응답을 제공한다."""
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from openai import APIConnectionError

from .history import DatabaseChatMessageHistory
from .models import ChatSession
from .views import owned_session
from .views_stream import _stream_events, classify_scope


OLLAMA_CONFIG_ERROR_MESSAGE = '서버의 Ollama 설정을 확인한다.'
OLLAMA_CONNECTION_ERROR_MESSAGE = (
    'Ollama에 연결하지 못했다. 로컬 Ollama 서버 또는 터널 주소를 확인한 뒤 다시 시도한다.'
)
OLLAMA_SCOPE_ERROR_MESSAGE = '질문 범위를 확인하지 못했다. 잠시 후 다시 시도한다.'


class OllamaNotConfigured(Exception):
    pass


def _ollama_model():
    """설정값을 검증하고 실제 전송 시에만 Ollama용 ChatOpenAI를 생성한다."""
    base_url = settings.OLLAMA_BASE_URL.strip()
    model_name = settings.OLLAMA_MODEL.strip()
    parsed = urlparse(base_url)
    try:
        timeout = int(settings.OLLAMA_TIMEOUT)
    except (TypeError, ValueError):
        raise OllamaNotConfigured from None
    if (not model_name or parsed.scheme not in {'http', 'https'} or not parsed.netloc
            or timeout <= 0):
        raise OllamaNotConfigured

    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=model_name,
        base_url=base_url,
        api_key='ollama',
        timeout=timeout,
        max_retries=0,
    )


@login_required
@require_GET
def ollama_index(request):
    session_id = request.GET.get('restore_sess_id')
    conversation = owned_session(request, session_id) if session_id else None
    return render(request, 'app/ollama.html', {
        'chat_messages': conversation.messages.all() if conversation else [],
        'session_id': str(conversation.pk) if conversation else '',
        'conversations': ChatSession.objects.filter(owner=request.user),
        'page_url_name': 'app:ollama_index',
        'chat_url_name': 'app:chat_ollama',
    })


@login_required
@require_POST
def chat_ollama(request):
    conversation = owned_session(request, request.POST.get('session_id'))
    query = request.POST.get('query', '').strip()
    if not query or len(query) > 2000:
        return JsonResponse({'error': '질문은 1~2000자로 입력한다.'}, status=400)

    try:
        model = _ollama_model()
        history = DatabaseChatMessageHistory(conversation, request.user)
        # 입력은 같은 최근 기록과 새 질문이고, 출력은 범위 판정 뒤 NDJSON 답변 스트림이다.
        messages = history.messages
        in_scope = classify_scope(query, messages, model)
    except OllamaNotConfigured:
        return JsonResponse({'error': OLLAMA_CONFIG_ERROR_MESSAGE}, status=503)
    except (APIConnectionError, ConnectionError, TimeoutError):
        return JsonResponse({'error': OLLAMA_CONNECTION_ERROR_MESSAGE}, status=502)
    except Exception:
        return JsonResponse({'error': OLLAMA_SCOPE_ERROR_MESSAGE}, status=502)

    response = StreamingHttpResponse(
        _stream_events(query, history, in_scope, messages, model),
        content_type='application/x-ndjson; charset=utf-8',
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response