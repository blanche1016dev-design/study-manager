from django import forms

from .models import LearningLog


class LeaningLogForm(forms.ModelForm):
    class Meta:
        model = LearningLog
        # ユーザーに入力させる項目を指定
        fields = ["subject", "content", "study_time"]
