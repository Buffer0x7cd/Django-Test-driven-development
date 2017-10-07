from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List
# Create your views here.

def home_page(request):
    ''' recieves item in form name item_text'''
    return render(request, 'lists/home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(item_list=list_)
    return render(request, 'lists/list.html', {'list':list_})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST.get('item_text'), item_list=list_)
    return redirect('/lists/{0}/'.format(list_.id))

def add_item(request, list_id):
    ''' add item to an existing list'''
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], item_list=list_)
    return redirect('/lists/{0}/'.format(list_.id))
