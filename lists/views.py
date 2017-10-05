from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item
# Create your views here.

def home_page(request):
    ''' recieves item in form name item_text'''
    if request.method == 'POST':
        item_text = request.POST['item_text']
        Item.objects.create(text=item_text)
        return redirect('/')
    
    items = Item.objects.all()
    return render(request, 'lists/home.html',
                  {'items':items})
