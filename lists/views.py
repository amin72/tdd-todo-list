from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List


def home_page(request):
    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items': items})


def list_view(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})


def new_list(request):
    list = List.objects.create()
    new_item_text = request.POST['item_text']
    Item.objects.create(text=new_item_text, list=list)
    return redirect('lists:list_view')
