from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.create, name='cards_make'),
    path('c/', views.see_card, name='cards_see'),
    # path('socomp/', views.changecurrent, name='cards_change'),
    path('tags/', views.taglist, name='cards_taglist'),
    path('t/<str:tag>',views.tagview, name='cards_tag'),
    path('del/', views.deltag, name='cards_deltag'),
    path('l/<str:tag>', views.card_list, name='cards_list'),
    path('url/', views.requestview, name='request_view')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)