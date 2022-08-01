from multiprocessing import AuthenticationError
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User

from butter.models import MyUser, Post

# ログインフォーム
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "
        for field in self.fields.values():
            field.widget.attrs['class'] = 'field-style form-field-style'
    
    username = forms.CharField(
        max_length = 20,
        widget = forms.TextInput(
            attrs={'placeholder':'E-mail'})
            )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={'placeholder':'Password'})
            )

    class Meta:
        fields = ('username', 'password')


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "
        for field in self.fields.values():
            field.widget.attrs['class'] = 'field-style form-field-style'

    username = forms.CharField(
        max_length = 20,
        widget = forms.TextInput(
            attrs={'placeholder':'User name'})
    )

    nickname = forms.CharField(
        max_length = 20,
        widget = forms.TextInput(
            attrs={'placeholder':'Nickname'})
    )

    email = forms.EmailField(
        max_length = 40,
        help_text = '必須 有効なメールアドレスを入力してください。',
        widget = forms.TextInput(
            attrs={'placeholder':'E-mail'}
        ),
    )

    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={'placeholder':'Password'}
        ),
    )

    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={'placeholder':'Password again'}
        ),
    )

    class Meta:
        model = MyUser
        fields = ('username', 'nickname', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('nickname', 'username', 'image', 'email', 'date_of_birth', 'url', 'introduction')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'field-style form-field-style', 'placeholder':'Username'}),
            'nickname': forms.TextInput(attrs={'class': 'field-style form-field-style', 'placeholder':'Name'}),
            'email': forms.TextInput(attrs={'class': 'field-style form-field-style', 'placeholder':'Email'}),
            'date_of_birth': forms.SelectDateWidget(years=[x for x in range(1920, 2022)], attrs={'class': 'field-style form-field-style date-field'}),
            'url': forms.TextInput(attrs={'class': 'field-style form-field-style', 'placeholder':'URL'}),
            'introduction': forms.Textarea(attrs={'class': 'field-style form-field-style textarea-style', 'placeholder':'Introduction', 'rows':3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "
        
            
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=("Old password"), widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=("New password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password again"), widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'field-style form-field-style'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_text',)
        labels = {'post_text':''}

        widgets = {
            'post_text': forms.Textarea(attrs={'rows':3, 'class': 'post-textfield-style', 'placeholder':'いまどうしてる？'}),
        }