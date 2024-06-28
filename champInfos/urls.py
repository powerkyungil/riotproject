from django.urls import path
from . import views

urlpatterns = [
    path('', views.champ_info, name='champ_info')
]
