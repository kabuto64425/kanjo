from django import forms

from .models import Shiwake

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