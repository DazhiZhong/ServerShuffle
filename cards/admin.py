from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Card)
admin.site.register(CardTags)
admin.site.register(UserCard)
admin.site.register(UserHashTag)
