from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    # 목록을 먼저 평가하지 않아 템플릿을 렌더링할 때 SQL이 실행된다.
    posts = Post.objects.order_by("pk")
    return render(request, "board/post_list.html", {
        "posts": posts,
        "detail_url_name": "board:fbv_detail",
        "list_url_name": "board:fbv_list",
        "page_label": "FBV 목록",
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "board/post_detail.html", {
        "post": post,
        "list_url_name": "board:fbv_list",
        "page_label": "FBV 상세",
    })