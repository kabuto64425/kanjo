from django import forms
from .models import User
from django.core import validators

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Column, Layout, HTML, Field

import logging

logger = logging.getLogger(__name__)

class UserUpdateForm(forms.Form):
    last_month = forms.IntegerField(label = '決算月', validators=[validators.MinValueValidator(1),
                    validators.MaxValueValidator(12)])
    last_day = forms.IntegerField(label = '決算日', validators=[validators.MinValueValidator(1),
                    validators.MaxValueValidator(31)])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Row(
                Column(
                    Field('last_month')
                    , css_class='form-group col'
                ),
                Column(
                    Field('last_day')
                    , css_class='form-group col'
                ),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        # もしすでにエラーがある場合は処理をスキップする
        if self.errors:
            return cleaned_data
        
        # 月、日の組み合わせがあり得るものか判定
        max_day = [31,29,31,30,31,30,31,31,30,31,30,31]
        if cleaned_data["last_day"] > max_day[cleaned_data["last_month"] - 1]:
            self.add_error(f'last_day', 'あり得る日を入力してください')

        return cleaned_data