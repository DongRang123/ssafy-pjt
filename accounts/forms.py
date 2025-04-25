from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from books.models import Category

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    # 관심 장르: Category에서 가져옴
    interested_genres = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="관심 장르"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'last_name',
            'first_name',
            'email',
            'gender',
            'age',
            'weekly_avg_reading_time',
            'annual_reading_amount',
            'profile_img',
            'interested_genres',
        )
        labels = {
            'username': '아이디',
            'last_name': '성',
            'first_name': '이름',
            'email': '이메일',
            'gender': '성별',
            'age': '나이',
            'weekly_avg_reading_time': '주간 평균 독서 시간',
            'annual_reading_amount': '연간 독서량',
            'profile_img': '프로필 사진',
            'interested_genres': '관심 장르',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "비밀번호"
        self.fields['password2'].label = "비밀번호 확인"

def save(self, commit=True):
    user = super().save(commit=False)
    if commit:
        user.save()
        self.save_m2m()  # ← 여기가 정답!
    return user

    

class CustomUserChangeForm(UserChangeForm):
    # 관심 장르 필드 (체크박스 + 복수 선택)
    interested_genres = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="관심 장르"
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            'username',
            'last_name',
            'first_name',
            'email',
            'gender',
            'age',
            'weekly_avg_reading_time',
            'annual_reading_amount',
            'profile_img',
            'interested_genres',
        )
        labels = {
            'username': '아이디',
            'last_name': '성',
            'first_name': '이름',
            'email': '이메일',
            'gender': '성별',
            'age': '나이',
            'weekly_avg_reading_time': '주간 평균 독서 시간',
            'annual_reading_amount': '연간 독서량',
            'profile_img': '프로필 사진',
            'interested_genres': '관심 장르',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')  # 비밀번호 필드 제거
        self.fields['interested_genres'].queryset = Category.objects.all() 


    def save(self, commit=True):
        user = super().save(commit=False)
        # genres = self.cleaned_data.get('interested_genres')
        # if genres:
        #     user.favorite_categories = ','.join([g.name for g in genres])
        # else:
        #     user.favorite_categories = ''
        if commit:
            user.save()
            self.save_m2m()
        return user