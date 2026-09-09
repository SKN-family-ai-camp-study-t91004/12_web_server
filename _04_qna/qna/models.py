from django.db import models
from django.contrib.auth.models import User

# Question(N) : User (1)
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='questions')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # - N:M 관계 -> 중간 테이블이 자동 생성
    # - 중간 테이블을 사용하기 위한 중간 모델의 이름
    voters = models.ManyToManyField(User, related_name='question_votes')

# Answer(N) : User (1)
# Answer(N) : Question (1)

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # N:M
    voters = models.ManyToManyField(User, related_name='answer_votes')