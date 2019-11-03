from django.urls import path
from . import views


app_name = 'lists'

urlpatterns = [
    path('<int:list_id>/', views.list_view, name='list_view'),
    path('new/', views.new_list, name='new_list'),
    path('<int:list_id>/add/', views.add_item, name='add_item'),
]
