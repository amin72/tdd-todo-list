from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item


def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('lists:list_view')
    else:
        items = Item.objects.all()
        return render(request, 'lists/home.html',
            {'items': items})


def list_view(request):
    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items': items})
