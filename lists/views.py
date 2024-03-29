from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List


def home_page(request):
    return render(request, 'lists/home.html')


def list_view(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'lists/list.html', {'items': items, 'list': list_})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('lists:list_view', list_id=list_.id)


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('lists:list_view', list_id=list_.id)
