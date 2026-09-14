"""DB 행을 LangChain 메시지로 변환한다. 인증된 사용자의 대화만 다룬다."""
from django.db import transaction
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from .models import ChatMessage, ChatSession


class DatabaseChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, conversation, owner):
        # View의 검사 외에도 저장소 경계에서 소유권을 다시 확인한다.
        self.conversation = ChatSession.objects.get(pk=conversation.pk, owner=owner)
        self.owner = owner

    @property
    def messages(self):
        # 최근 메시지 20개를 읽은 뒤 시간순으로 바꾼다. 토큰 20개 또는 대화 20쌍이 아니다.
        rows = list(ChatMessage.objects.filter(
            conversation=self.conversation, conversation__owner=self.owner,
        ).order_by('-created_at', '-pk')[:20])
        return [HumanMessage(content=row.content) if row.message_type == 'human'
                else AIMessage(content=row.content) for row in reversed(rows)]

    def add_messages(self, messages):
        rows = []
        for message in messages:
            if not isinstance(message, (HumanMessage, AIMessage)) or not isinstance(message.content, str):
                raise ValueError('텍스트 human/ai 메시지만 저장한다.')
            rows.append(ChatMessage(
                conversation=self.conversation, session_id=str(self.conversation.pk),
                message_type='human' if isinstance(message, HumanMessage) else 'ai',
                content=message.content,
            ))
        # 사람·AI 두 메시지가 함께 저장되거나 함께 취소되도록 처리한다.
        # bulk_create() : 대량/일괄 생성(대량/일괄 UPSERT)
        with transaction.atomic():
            ChatSession.objects.get(pk=self.conversation.pk, owner=self.owner)
            ChatMessage.objects.bulk_create(rows)

    def clear(self):
        ChatMessage.objects.filter(conversation=self.conversation,
                                   conversation__owner=self.owner).delete()