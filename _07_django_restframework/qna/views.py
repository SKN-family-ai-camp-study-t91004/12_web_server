from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .models import Question, Answer
from .permissions import IsOwnerOrReadOnly
from .serializers import QuestionSerializer, AnswerSerializer


class OwnedModelViewSet(ModelViewSet):
    # Router가 GET 목록을 list, POST 목록을 create 등으로 연결한다. 같은 자원의 CRUD를 상속한다.
    # 첫 권한은 비로그인 쓰기를, 둘째 권한은 타인의 객체 수정을 막는다.
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # JSON의 author를 신뢰하지 않고 SessionAuthentication의 사용자로 저장한다.
        # Serializer를 통과한 subject/content와 이 author가 합쳐져 새 객체가 되고 HTTP 201 데이터가 된다.
        serializer.save(author=self.request.user)


class QuestionViewSet(OwnedModelViewSet):
    # 추천자 목록을 미리 읽고, 같은 시각의 글은 PK로 정렬을 고정한다.
    queryset = Question.objects.prefetch_related('voters').order_by('-created_at', '-pk')
    serializer_class = QuestionSerializer


class AnswerViewSet(OwnedModelViewSet):
    queryset = Answer.objects.prefetch_related('voters').order_by('pk')
    serializer_class = AnswerSerializer