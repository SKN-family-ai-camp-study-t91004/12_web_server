# Question과 Answer는 FK로 연결하고 추천자는 별도 중간 테이블로 관리한다.
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='questions')
    subject = models.CharField(max_length=200) # null=False, blank=False(폼유효성검사)
    content = models.TextField() # null=False, blank=False(폼유효성검사)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    voters = models.ManyToManyField(User, blank=True, related_name='question_votes') # null옵션은 ManyToManyField에서 사용하지 않음


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    voters = models.ManyToManyField(User, blank=True, related_name='answer_votes')