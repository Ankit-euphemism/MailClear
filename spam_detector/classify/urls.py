from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.classify_email, name='classify_email'),
]