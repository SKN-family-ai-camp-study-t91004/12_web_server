# 인증용 User와 생일·프로필 정보는 OneToOneField로 연결한다.
from django.db import models
from django.contrib.auth.models import User


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    profile = models.ImageField(upload_to='profile/', null=True, blank=True) 


