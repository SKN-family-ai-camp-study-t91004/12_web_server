from django.urls import path

from . import views_fbv
from .views_cbv import PostCreateView, PostDetailView, PostListView

app_name = "board"

urlpatterns = [
    path("", views_fbv.post_list, name="home"),
    path("fbv/", views_fbv.post_list, name="fbv_list"),
    path("fbv/<int:pk>/", views_fbv.post_detail, name="fbv_detail"),

    # as_view(): View 클래스에 정의된 내용을 토대로
    #            요청을 받을 때 마다 Django가 View 함수 형태로 변환해준다.
    path("cbv/", PostListView.as_view(), name="cbv_list"),
    path("cbv/new/", PostCreateView.as_view(), name="cbv_create"),
    path("cbv/<int:pk>/", PostDetailView.as_view(), name="cbv_detail"),
]