from django import forms
from .models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'nick_name',
        ]
    
    def __init__(self, nick_name=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if nick_name:
            self.fields['nick_name'].initial = nick_name

    def update(self, user):
        user.nick_name = self.cleaned_data['nick_name']
        user.save()