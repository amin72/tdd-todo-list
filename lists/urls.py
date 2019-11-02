from django.urls import path
from . import views


app_name = 'lists'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('lists/the-only-list-in-the-world/', views.list_view, name='list_view'),
]
