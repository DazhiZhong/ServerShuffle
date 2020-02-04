from django import forms
from .models import *


class FilePostForm(forms.ModelForm):
    
    class Meta:
        model = FilePost
        fields = ("name","upload_file")

