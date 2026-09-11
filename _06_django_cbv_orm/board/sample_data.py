"""반복 실행해도 중복되지 않는 수업용 데이터를 만든다."""
from .models import Author, Comment, Post


def prepare_sample_data():
    authors = []
    for name in ["민지", "준호"]:
        # get_or_create는 (객체, 새로 만들었는지) 튜플을 반환한다.
        author, _ = Author.objects.get_or_create(name=name)
        authors.append(author)

    post_specs = [
        (authors[0], "Django 첫 글", "모델과 URL을 연결하는 첫 실습이다."),
        (authors[1], "FBV와 CBV", "같은 화면을 두 뷰 방식으로 만든다."),
        (authors[0], "ORM 쿼리", "select_related와 prefetch_related를 비교한다."),
    ]
    created_posts = 0
    created_comments = 0
    for author, title, content in post_specs:
        post, created = Post.objects.get_or_create(
            title=title,
            # defaults는 새 Post를 만들 때만 적용해 기존 글을 바꾸지 않는다.
            defaults={"author": author, "content": content},
        )
        created_posts += int(created)
        for number in [1, 2]:
            _, comment_created = Comment.objects.get_or_create(
                post=post,
                content=f"{title}의 댓글{number}",
            )
            created_comments += int(comment_created)

    return {
        "created_posts": created_posts,
        "created_comments": created_comments,
        "total_authors": Author.objects.count(),
        "total_posts": Post.objects.count(),
        "total_comments": Comment.objects.count(),
    }