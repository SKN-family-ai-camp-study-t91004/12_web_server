from django.contrib import admin
from .models import Post

# @ == 데코레이터: 해당 변수/함수/클래스에 대한 지시문을 작성

# 관리자 페이지에 Post 모델 관리 화면을 등록하는 역할의 클래스
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')