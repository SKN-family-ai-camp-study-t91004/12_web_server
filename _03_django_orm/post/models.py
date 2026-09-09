from django.db import models

# Create your models here.

# 모델 클래스는 테이블, 인스턴스는 한 행에 대응한다. id 기본키는 Django가 추가한다.
class Post(models.Model):

    # 클래스 작성만으로 테이블은 생기지 않는다. makemigrations로 기록하고 migrate로 적용한다.
    title = models.CharField(max_length=100)  # 길이 제한이 있는 제목이다.
    content = models.TextField()  # 본문처럼 긴 문자열을 저장한다.
    created_at = models.DateTimeField(auto_now_add=True)  # 최초 INSERT 시각이다.
    updated_at = models.DateTimeField(auto_now=True)  # 인스턴스 save() 시 갱신한다.

    def __str__(self):
        # Admin의 선택 목록과 shell에서 객체를 식별할 때 사용한다.
        return self.title
