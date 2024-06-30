from django.urls import path
from . import views

urlpatterns = [
    path('record_search', views.record_search, name='record_search'),
]
