from django import forms
from .models import DiaryPost

class DiaryPostForm(forms.ModelForm):
    class Meta:
        model = DiaryPost
        fields = ("title", "content")
        exclude = ["diary_user"]
