"""프로젝트 URL은 board 앱으로 전달한다."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("board.urls")),
]