from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List
# Create your views here.

def home_page(request):
    ''' recieves item in form name item_text'''
    return render(request, 'lists/home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items':items})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST.get('item_text'), item_list=list_)
    return redirect('/lists/the-only-list-in-the-world/')
