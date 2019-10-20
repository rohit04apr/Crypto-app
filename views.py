from django.shortcuts import render, redirect
from .models import list
from .forms import listForm
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
    import requests
    import json

    # Grab crypto price data
    price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,XRP&tsyms=USD,EUR")
    price = json.loads(price_request.content)

    # Grab crypto News
    api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    api = json.loads(api_request.content)
    return render(request, 'home.html', {'api': api, 'price': price })


def about(request):
    return render(request, 'about.html', {})

def todo(request):

    if request.method == 'POST':
        form = listForm(request.POST or None)
        if form.is_valid():
            form.save()
            all_items = list.objects.all
            messages.success(request, ('Item Has Been Added To List!'))
            return render(request, 'todo.html', {'all_items': all_items})
    else:
        all_items = list.objects.all
        return render(request, 'todo.html', {'all_items': all_items})


def delete(request, list_id):
    item = list.objects.get(pk=list_id)
    item.delete()
    messages.success(request, ('Item Has Been Deleted!'))
    return redirect('todo')

def cross_off(request, list_id):
    item = list.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect('todo')

def uncross(request, list_id):
    item = list.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect('todo')

def edit(request, list_id):
    if request.method == 'POST':
        item = list.objects.get(pk=list_id)

        form = listForm(request.POST or None, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, ('Item Has Been Edited!'))
            return redirect('todo')
    else:
        item = list.objects.get(pk=list_id)
        return render(request, 'edit.html', {'item': item})
