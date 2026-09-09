from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    # UserCreationForm이 비밀번호 검증·해시를 처리하고 프로필 정보는 별도 모델에 저장한다.
    birthday = forms.DateField(label='Birthday', required=False)
    profile = forms.ImageField(label='Profile', required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def clean_username(self):
        # 부모의 아이디 중복 검사를 유지하고 수업의 길이 규칙을 추가한다.
        username = super().clean_username()
        if len(username) < 4:
            raise forms.ValidationError('아이디는 4글자 이상이어야 한다.')
        return username

    def clean_profile(self):
        # ImageField가 이미지인지 확인한 업로드 객체에 용량 제한을 더한다.
        # 성공한 반환값은 cleaned_data['profile']을 거쳐 UserDetail 저장에 사용한다.
        profile = self.cleaned_data.get('profile')
        if profile and profile.size > 5 * 1024 * 1024:
            raise forms.ValidationError('프로필은 5MB 이하로 업로드한다.')
        return profile
