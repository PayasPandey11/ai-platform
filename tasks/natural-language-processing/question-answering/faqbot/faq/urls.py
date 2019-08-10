from django.urls import path
from . import views as views


urlpatterns = [
    path('ask', views.ask, name='chat'),
    path('train', views.train, name='train'),
]