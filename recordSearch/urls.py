from django.urls import path
from . import views

urlpatterns = [
    path('', views.record_search, name='record_search'),
]
