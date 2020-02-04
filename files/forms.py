from django import forms
from .models import *
from s3direct.widgets import S3DirectWidget

class S3DirectUploadForm(forms.Form):
    images = forms.URLField(widget=S3DirectWidget(dest='example_destination'))

# class UpForm(forms.ModelForm):

#     class Meta:
#         model = ExampleFile
#         fields = ['uploadfile']

class FilePostForm(forms.ModelForm):
    
    class Meta:
        model = FilePost
        fields = ("name","upload_file")

