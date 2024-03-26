from django import forms
from .models import Shiwake, Kanjo

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Column, Layout, HTML

class TestForm(forms.Form):
    shiwake_date = forms.DateField(label = '仕訳日')

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        for i in range(1, 11):  # 10個のフィールドを追加
            self.fields[f'kari_kanjo_kamoku_{i}'] = forms.CharField(label=f"勘定科目", max_length=100)
            self.fields[f'kari_amount_{i}'] = forms.IntegerField(label=f"金額")
            self.fields[f'kashi_kanjo_kamoku_{i}'] = forms.CharField(label=f"勘定科目", max_length=100)
            self.fields[f'kashi_amount_{i}'] = forms.IntegerField(label=f"金額")
        
        self.helper = FormHelper()
        rows = [Row(
                Column(f'kari_kanjo_kamoku_{i}', css_class='form-group col-md-3 mb-0'),
                Column(f'kari_amount_{i}', css_class='form-group col-md-3 mb-0'),
                Column(f'kashi_kanjo_kamoku_{i}', css_class='form-group col-md-3 mb-0'),
                Column(f'kashi_amount_{i}', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ) for i in range(1, 11)]
        self.helper.layout = Layout(
            Row(
                Column('shiwake_date', css_class='form-group col'),
                css_class='form-row'
            ),
            Row(
                Column(HTML("<div class='text-center'>借方</div>")),
                Column(HTML("<div class='text-center'>貸方</div>")),
            ),
            *rows
        )

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