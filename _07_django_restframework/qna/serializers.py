from rest_framework import serializers
from .models import Question, Answer


# 요청 JSON → 검증된 필드 → 모델로 변환하며, 응답에서는 모델을 JSON 자료로 변환한다.
class QuestionSerializer(serializers.ModelSerializer):
    # data={'subject': '질문', 'content': '본문'} → is_valid() → validated_data 순서로 검증한다.
    # 검증 실패 시 errors에서 필드별 원인을 확인하고, 성공한 값만 validated_data로 읽는다.
    # 검증만으로 저장되지 않는다. ViewSet의 perform_create에서 save(author=...)를 호출한다.
    class Meta:
        model = Question
        fields = ['id', 'author', 'subject', 'content', 'created_at', 'modified_at', 'voters']
        # 입력 author=999를 보내도 validated_data에는 들어가지 않는다. 응답에는 작성자 PK가 표시된다.
        read_only_fields = ['id', 'author', 'created_at', 'modified_at', 'voters']


class AnswerSerializer(serializers.ModelSerializer):
    # 입력 question=12 → 존재하는 Question 객체인지 검증 → 답변의 FK로 저장한다.
    # 응답은 질문 전체를 중첩하지 않고 question의 PK를 반환한다.
    class Meta:
        model = Answer
        fields = ['id', 'author', 'question', 'content', 'created_at', 'modified_at', 'voters']
        read_only_fields = ['id', 'author', 'created_at', 'modified_at', 'voters']