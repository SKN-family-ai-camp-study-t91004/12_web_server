"""로그인 사용자 → 상담 세션 → 메시지 관계를 DB에 저장한다."""
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at', '-pk']


class ChatMessage(models.Model):
    # 이전 예제의 식별자는 데이터 보존용이다. 접근 권한은 conversation.owner로 판단한다.
    session_id = models.CharField(max_length=255, db_index=True, blank=True, default='')
    # 기존 메시지의 소유자를 추측해 연결하지 않는다. 신규 메시지는 반드시 대화에 연결한다.
    conversation = models.ForeignKey(ChatSession, on_delete=models.CASCADE,
                                     related_name='messages', null=True)
    message_type = models.CharField(max_length=10, choices=[('human', 'Human'), ('ai', 'AI')])
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at', 'pk']

    def __str__(self):
        return f'{self.message_type}: {self.content[:30]}'