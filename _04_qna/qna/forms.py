from django import forms
from .models import Question, Answer

# fields : 꼭 입력 받아야하는 필드 목록
# 작성자(author), 추천자(voter)는 서버가 결정한다.
class QuestionForm(forms.ModelForm):

    # HTTP Method = POST 요청 시
    # subject·content → 필수 여부·최대 길이 검증
    # → cleaned_data → View의 저장 분기에 사용한다.

    class Meta:
        model = Question
        fields = ['subject', 'content']
        labels = {'subject': '제목', 'content': '내용'}


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {'content': '답변 내용'}