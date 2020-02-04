from django.db import models

from s3direct.fields import S3DirectField
# Create your models here.


# class FileUpload(models.Model):

#     file = models.FileField(upload_to='uploaded_content',storage=[...])

# class ExampleFile(models.Model):
#     uploadfile = S3DirectField(dest='example_destination')


class Example(models.Model):
    video = S3DirectField(dest='example_destination')

class FilePost(models.Model):
    name = models.CharField(max_length=50)
    upload_file = models.FileField(upload_to="post_files")
    


    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("FilePost_detail", kwargs={"pk": self.pk})

