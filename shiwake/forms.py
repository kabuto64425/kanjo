from django import forms
from .models import Shiwake, Kanjo
from app.models import MasterKanjoKamoku
from config.consts import KANJO_ROWS
from django.core import validators

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Column, Layout, HTML, Field

import logging

logger = logging.getLogger(__name__)

class ShiwakeForm(forms.Form):
    shiwake_date = forms.DateField(label = '仕訳日')

    def __init__(self, *args, **kwargs):
        super(ShiwakeForm, self).__init__(*args, **kwargs)
        for i in range(1, KANJO_ROWS + 1):
            self.fields[f'kari_kanjo_kamoku_{i}'] = forms.ModelChoiceField(label=f"", queryset=MasterKanjoKamoku.objects, required=False)
            self.fields[f'kari_amount_{i}'] = forms.IntegerField(label=f"", required=False, widget=forms.TextInput, validators=[validators.MinValueValidator(0)])
            self.fields[f'kashi_kanjo_kamoku_{i}'] = forms.ModelChoiceField(label=f"", queryset=MasterKanjoKamoku.objects, required=False)
            self.fields[f'kashi_amount_{i}'] = forms.IntegerField(label=f"", required=False, widget=forms.TextInput, validators=[validators.MinValueValidator(0)])
        
        self.helper = FormHelper()
        rows = [Row(
                Column(Field(f'kari_kanjo_kamoku_{i}'), css_class='form-group col-md-3 mb-0'),
                Column(Field(f'kari_amount_{i}', css_class='text-right'), css_class='form-group col-md-3 mb-0'),
                Column(Field(f'kashi_kanjo_kamoku_{i}'), css_class='form-group col-md-3 mb-0'),
                Column(Field(f'kashi_amount_{i}', css_class='text-right'), css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ) for i in range(1, KANJO_ROWS + 1)]
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('shiwake_date')
                    , css_class='form-group col'
                ),
                css_class='form-row'
            ),
            Row(
                Column(HTML("<div class='text-center'>借方</div>")),
                Column(HTML("<div class='text-center'>貸方</div>")),
            ),
            *rows,
            Row(
                Column(HTML("<input disabled class='textinput textInput form-control' value='合計'/>")),
                Column(HTML("<input disabled id='kari_sum' class='text-right textinput textInput form-control'/>")),
                Column(HTML("<input disabled class='textinput textInput form-control' value='合計'/>")),
                Column(HTML("<input disabled id='kashi_sum' class='text-right textinput textInput form-control'/>")),
            ),
        )
    
    def clean(self):
        cleaned_data = super().clean()
        data = self.data
        for i in range(1, KANJO_ROWS + 1):
            # 借方
            if not data.get(f'kari_kanjo_kamoku_{i}') and data.get(f'kari_amount_{i}'):
                self.add_error(f'kari_kanjo_kamoku_{i}', '勘定科目を入力してください')
            if data.get(f'kari_kanjo_kamoku_{i}') and not data.get(f'kari_amount_{i}'):
                self.add_error(f'kari_amount_{i}', '金額を入力してください')
            # 貸方
            if not data.get(f'kashi_kanjo_kamoku_{i}') and data.get(f'kashi_amount_{i}'):
                self.add_error(f'kashi_kanjo_kamoku_{i}', '勘定科目を入力してください')
            if data.get(f'kashi_kanjo_kamoku_{i}') and not data.get(f'kashi_amount_{i}'):
                self.add_error(f'kashi_amount_{i}', '金額を入力してください')
        
        # もしすでにエラーがある場合は処理をスキップする
        if self.errors:
            return cleaned_data
        
        # TODO貸借一致チェック
        kari_amout_sum = sum([cleaned_data.get(f'kari_amount_{i}') if cleaned_data.get(f'kari_amount_{i}') else 0 for i in range(1, KANJO_ROWS + 1)])
        kashi_amout_sum = sum([cleaned_data.get(f'kashi_amount_{i}') if cleaned_data.get(f'kashi_amount_{i}') else 0 for i in range(1, KANJO_ROWS + 1)])
        if kari_amout_sum != kashi_amout_sum:
            self.add_error(None, '借方の合計と貸方の合計を一致させてください')
        return cleaned_data
    
    def is_valid(self):
        valid = super().is_valid()
        if self.cleaned_data.get(f'kari_kanjo_kamoku_{1}'):
            logger.info(True)
        else:
            logger.info(False)
        return valid