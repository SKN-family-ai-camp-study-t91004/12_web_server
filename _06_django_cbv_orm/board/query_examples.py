"""관계 객체를 읽는 ORM 쿼리 수를 비교하는 함수 모음이다."""
from django.db import connection
from django.db.models import Count
from django.test.utils import CaptureQueriesContext

from .models import Post


def _measure(queryset, row_builder):
    # QuerySet 평가와 관계 접근을 캡처 구간 안에서 함께 실행한다.
    with CaptureQueriesContext(connection) as captured:
        rows = [row_builder(post) for post in queryset]
    return {"rows": rows, "query_count": len(captured)}


def compare_author_queries():
    # 기본 방식, 최적화 방식 비교
    # - 두 측정은 별도의 QuerySet을 만들어서
    # 서로 값을 공유하지 않는 상태를 만든다.

    # QuerySet: select 결과의 각 행을 저장한 Model 객체 집합

    """작성자 접근의 N+1 쿼리와 select_related 결과를 비교한다."""
    plain = _measure(
        Post.objects.order_by("pk")[:3],
        lambda post: (post.pk, post.title, post.author.name),
    )
    optimized = _measure(
        # select_related("author")
        # - Post와 Author 테이블을 JOIN해서 SELECT를 1회만 실행
        Post.objects.select_related("author").order_by("pk")[:3],
        lambda post: (post.pk, post.title, post.author.name),
    )
    return {"plain": plain, "optimized": optimized}


def compare_comment_queries():
    """역참조 댓글 접근의 N+1 쿼리와 prefetch_related 결과를 비교한다."""
    plain = _measure(

        # Post 테이블 모든 데이터 중 pk 오름차순으로 3행만 조회
        # - Post는 Author와 N:1 (FK) 관계를 맺고 있음
        # - Django ORM은 Model(Post) 조회 시
        # 자동으로 관계를 맺은 테이블(Author)을 조회함
        # -> 이때, 조회 방식은 Post의 각 행에 접근하며
        #   Author의 pk 값을 얻어와 Author 테이블에서 select 1회 시도
        # -> Post 1회, Post 조회 행 수 만큼 Author 조회(3회)
        #   total : 4회
        Post.objects.order_by("pk")[:3],
        lambda post: (post.pk, post.title, [comment.content for comment in post.comments.all()]),
    )
    optimized = _measure(

        # 1:N 관계에서는 prefetch_related() 사용

        # Post.objects.prefetch_related("comments")
        # - Post를 1회 조회하고, 관계를 맺은 Comment도 1회만 조회 후
        # 두 조회 결과를 장고 서버 메모리에서 연결하는 작업을 수행

        Post.objects.prefetch_related("comments").order_by("pk")[:3],
        # all()은 prefetch_related가 채운 역참조 캐시를 사용한다.
        lambda post: (post.pk, post.title, [comment.content for comment in post.comments.all()]),
    )
    return {"plain": plain, "optimized": optimized}


# Post 별로 Comment가 몇 개 작성되어 있는지 숫자 조회
def show_comment_counts():
    """Count 집계로 게시글별 댓글 수를 한 번의 쿼리로 읽는다."""
    with CaptureQueriesContext(connection) as captured:
        rows = [(post.title, post.comment_count) for post in (
            # Post.objects.annotate(comment_count=Count("comments"))
            # - Post 1회 조회 + Comment N번 조회
            # - 단, Comment 조회 시 본문 전체가 아닌 행의 개수만 Count
            Post.objects.annotate(comment_count=Count("comments")).order_by("pk")[:3]
        )]
    return {"rows": rows, "query_count": len(captured)}