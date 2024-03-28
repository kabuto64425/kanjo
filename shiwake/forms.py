from django import forms
from .models import Shiwake, Kanjo
from app.models import MasterKanjoKamoku
from config.consts import KANJO_ROWS
from django.core import validators

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Column, Layout, HTML, Field

import logging

logger = logging.getLogger(__name__)

class TestForm(forms.Form):
    shiwake_date = forms.DateField(label = '仕訳日')

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        for i in range(1, KANJO_ROWS + 1):
            self.fields[f'kari_kanjo_kamoku_{i}'] = forms.ModelChoiceField(label=f"", queryset=MasterKanjoKamoku.objects, required=False)
            self.fields[f'kari_amount_{i}'] = forms.IntegerField(label=f"", required=False, validators=[validators.MinValueValidator(0)])
            self.fields[f'kashi_kanjo_kamoku_{i}'] = forms.ModelChoiceField(label=f"", queryset=MasterKanjoKamoku.objects, required=False)
            self.fields[f'kashi_amount_{i}'] = forms.IntegerField(label=f"", required=False, validators=[validators.MinValueValidator(0)])
        
        self.helper = FormHelper()
        rows = [Row(
                Column(f'kari_kanjo_kamoku_{i}', css_class='form-group col-md-3 mb-0'),
                Column(f'kari_amount_{i}', css_class='form-group col-md-3 mb-0'),
                Column(f'kashi_kanjo_kamoku_{i}', css_class='form-group col-md-3 mb-0'),
                Column(f'kashi_amount_{i}', css_class='form-group col-md-3 mb-0'),
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
            *rows
        )
    
    def clean(self):
        cleaned_data = super().clean()
        for i in range(1, KANJO_ROWS + 1):
            # 借方
            if not cleaned_data.get(f'kari_kanjo_kamoku_{i}') and cleaned_data.get(f'kari_amount_{i}'):
                self.add_error(f'kari_kanjo_kamoku_{i}', '勘定科目を入力してください')
                #raise forms.ValidationError("Field1とField2の値が一致しません。")
            if cleaned_data.get(f'kari_kanjo_kamoku_{i}') and not cleaned_data.get(f'kari_amount_{i}'):
                self.add_error(f'kari_amount_{i}', '金額を入力してください')
                #raise forms.ValidationError("Field1とField2の値が一致しません。")
            # 貸方
            if not cleaned_data.get(f'kashi_kanjo_kamoku_{i}') and cleaned_data.get(f'kashi_amount_{i}'):
                self.add_error(f'kashi_kanjo_kamoku_{i}', '勘定科目を入力してください')
                #raise forms.ValidationError("Field1とField2の値が一致しません。")
            if cleaned_data.get(f'kashi_kanjo_kamoku_{i}') and not cleaned_data.get(f'kashi_amount_{i}'):
                self.add_error(f'kashi_amount_{i}', '金額を入力してください')
                #raise forms.ValidationError("Field1とField2の値が一致しません。")
        
        # もしすでにエラーがある場合は処理をスキップする
        if self.errors:
            return cleaned_data
        
        # TODO貸借一致チェック
        for i in range(1, KANJO_ROWS + 1):
                pass
                #for cleaned_data.get(f'kari_amount_{i}')
        
        self.add_error(None, 'aaaaa')
        return cleaned_data
    
    def is_valid(self):
        valid = super().is_valid()
        if self.cleaned_data.get(f'kari_kanjo_kamoku_{1}'):
            logger.info(True)
        else:
            logger.info(False)
        return valid

# 追加
class ModelFormWithFormSetMixin:

    def __init__(self, *args, **kwargs):
        super(ModelFormWithFormSetMixin, self).__init__(*args, **kwargs)
        self.formset = self.formset_class(
            instance=self.instance,
            data=self.data if self.is_bound else None,
        )

    def is_valid(self):
        return super(ModelFormWithFormSetMixin, self).is_valid() and self.formset.is_valid()

    def save(self, commit=True):
        saved_instance = super(ModelFormWithFormSetMixin, self).save(commit)
        1/0
        self.formset.save(commit)
        return saved_instance

class KanjoForm(forms.ModelForm):
    class Meta:
        model = Kanjo
        fields = '__all__'
    
KanjoFormSet = forms.inlineformset_factory(
    parent_model=Shiwake,
    model=Kanjo,
    form=KanjoForm,
    extra=3
)

class ShiwakeForm_temp2(ModelFormWithFormSetMixin, forms.ModelForm):

    formset_class = KanjoFormSet

    class Meta:
        model = Shiwake
        fields = '__all__'

class ShiwakeForm_temp(forms.Form):
    shiwake_date = forms.DateField()

class ShiwakeForm(forms.ModelForm):
    """
    モデルフォーム構成クラス
    ・公式 モデルからフォームを作成する
    https://docs.djangoproject.com/ja/2.1/topics/forms/modelforms/
    """

    class Meta:
        model = Shiwake
        fields = '__all__'

        # 以下のフィールド以外が入力フォームに表示される
        # AutoField
        # auto_now=True
        # auto_now_add=Ture
        # editable=False
    
    def save(self, commit=True):
        instance = super(ShiwakeForm, self).save(commit=commit)

        if commit:
            instance.save()

        return instance