from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch-data/', views.fetch_data, name='fetch_data'),
]