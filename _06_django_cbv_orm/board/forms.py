from django import forms

from .models import Post

# ModelForm
# - 모델 필드와 검증 규칙을 HTML 폼에 연결
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["author", "title", "content"]
        labels = {"author": "작성자", "title": "제목", "content": "내용"}

        # widgets : 화면에 어떤 HTML 입력 요소로 그릴지 커스텀
        widgets = {
            "author": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "글 제목"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "글 내용"}),
        }