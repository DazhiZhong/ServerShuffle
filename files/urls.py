from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #path(''),
    path('file/',views.upload_file,name='upload_file'),
    path('files/',views.files,name='files'),
    path('up/', views.MyView.as_view(), name = 'up')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)