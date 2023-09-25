from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('', views.main, name='main'),
    path('create_author', views.create_author, name='create_author'),
    path('author/<int:author_id>', views.author, name='author'),
]
