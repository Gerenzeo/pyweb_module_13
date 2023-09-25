from django.urls import path
from . import views

app_name = 'tags'

urlpatterns = [
    path('tag/<str:tagname>', views.tag, name='tag'),
    path('create_tag', views.create_tag, name='create_tag'),
]
