from django import forms
from .models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Column, Layout, HTML, Field

import logging

logger = logging.getLogger(__name__)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'last_month',
            'last_day'
        ]
    
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
        logger.info(cleaned_data.get('last_month'))
        if self.errors:
            return cleaned_data

        max_day = [31,29,31,30,31,30,31,31,30,31,30,31]
        if cleaned_data["last_day"] > max_day[cleaned_data["last_month"] - 1]:
            self.add_error(f'last_day', 'あり得る日を入力してください')

        return cleaned_data