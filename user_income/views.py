from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
import json

@login_required(login_url='authentication/login')
def index(request):
    source = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='authentication/login')
def add_income(request):
    source = Source.objects.all()
    context = {
        'source': source,
        'values': request.POST
    }
    if request.method == 'GET':

        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Please enter amount.')
            return render(request, 'income/add_income.html', context)

        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Description cannot be empty.')
            return render(request, 'income/add_income.html', context)

        UserIncome.objects.create(owner=request.user ,amount=amount, description=description, date=date, source=source)
        messages.success(request, 'Record successfully added.')

        return redirect('income')

@login_required(login_url='authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources,
    }
    if request.method == 'GET':
        return render(request, 'income/edit-income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Please enter amount.')
            return render(request, 'income/edit-income.html', context)

        description = request.POST['description']
        date = request.POST['income_date']
        sources = request.POST['source']

        if not description:
            messages.error(request, 'Description cannot be empty.')
            return render(request, 'income/edit-income.html', context)

        income.owner = request.user
        income.amount=amount
        income.description=description
        income.date=date
        income.source=sources
        income.save()
        messages.success(request, 'Record successfully updated.')

        return redirect('income')

@login_required(login_url='authentication/login')
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Record successfully deleted.')
    return redirect('income')

def search_income(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')

        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)

        data = income.values()
        return JsonResponse(list(data), safe=False)