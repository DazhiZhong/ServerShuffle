from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CardTags(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name


class Card(models.Model):
    title = models.CharField(blank = True, null=True, max_length=100)
    txt = models.TextField()
    tags = models.CharField(max_length=100, blank=True, null=True, default="")
    def __str__(self):
        return self.title+'-'+self.txt+' '+self.tags

    def get_absolute_url(self):
        return reverse("Card_detail", kwargs={"pk": self.pk})

class UserCard(models.Model):

    title = models.CharField(blank = True, null=True, max_length=100)
    txt = models.TextField(blank = True, null=True )
    tags = models.CharField(max_length=100, blank=True, null=True, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse("Card_detail", kwargs={"pk": self.pk})

class UserHashTag(models.Model):

    name = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ManyToManyField(UserCard)

    def __str__(self):
        return self.name

class CurrentDeck(models.Model):

    tags = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        pass


