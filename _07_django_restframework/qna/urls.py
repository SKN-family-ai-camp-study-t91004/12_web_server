from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet

# Router가 목록 GET/POST와 상세 GET/PUT/PATCH/DELETE 경로를 만든다.

# register()의 첫 인자는 URL 자원명, 둘째 인자는 그 자원의 CRUD를 처리할 ViewSet 클래스이다.
# queryset이 있으므로 basename은 모델명에서 추론되어 question-list, question-detail 같은 역방향 이름도 만든다.
# ex) GET /api/questions/는 QuestionViewSet.list, POST는 create, GET /api/questions/12/는 retrieve로 연결된다
router = DefaultRouter()
router.register('questions', QuestionViewSet)
router.register('answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls))
]