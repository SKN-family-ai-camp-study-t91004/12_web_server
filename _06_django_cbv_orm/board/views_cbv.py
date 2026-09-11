from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from .forms import PostForm
from .models import Post

# 게시글 "목록 조회" View - ListView 상속
class PostListView(ListView):
    model = Post
    template_name = "board/post_list.html"
    # ListView 기본 이름 object_list 대신 템플릿의 posts를 사용한다.
    context_object_name = "posts"
    ordering = ["pk"]

    def get_context_data(self, **kwargs):
        # 부모가 만든 posts 문맥을 먼저 유지한 뒤 화면용 값을 더한다.

        # 부모(ListView)가 지정된 모델(Post) 테이블에서 목록 조회를 자동 실행
        # -> 조회가 완료되면 부모의 context에 담아둔다
        context = super().get_context_data(**kwargs)

        context.update({
            "detail_url_name": "board:cbv_detail",
            "list_url_name": "board:cbv_list",
            "page_label": "CBV 목록",
        })
        return context

# DetailView : 상세 조회 View -> pk가 필수로 전달 되어야 한다
class PostDetailView(DetailView):
    model = Post
    template_name = "board/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"list_url_name": "board:cbv_list", "page_label": "CBV 상세"})
        return context

# CreateView : Insert 용도의 View
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "board/post_form.html"

    # INSERT 성공 시 라다이렉트 할 URL 반환
    def get_success_url(self):
        # 저장된 self.object의 pk를 상세 URL 인자로 전달한다.
        return reverse("board:cbv_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"list_url_name": "board:cbv_list", "page_label": "CBV 글 작성"})
        return context