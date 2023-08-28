from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('create_quote', views.create_quote, name='create_quote'),
    path('', views.quote_detail, name='quote_detail'),
]
