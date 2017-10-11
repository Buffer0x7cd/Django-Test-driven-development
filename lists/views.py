from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List
from django.core.exceptions import ValidationError
# Create your views here.

def home_page(request):
    ''' recieves item in form name item_text'''
    return render(request, 'lists/home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.POST:
        Item.objects.create(text= request.POST.get('item_text'), item_list=list_)
        return redirect('/lists/{0}/'.format(list_.id))
    return render(request, 'lists/list.html', {'list':list_})

def new_list(request):
    list_ = List.objects.create()
    tmpItem = Item(text=request.POST.get('item_text'), item_list=list_)
    try:
        tmpItem.full_clean()
    except ValidationError:
        list_.delete()
        error = "you can't submit empty list items"
        return render(request, 'lists/home.html', {'error':error})
    tmpItem.save()
    return redirect('/lists/{0}/'.format(list_.id))
