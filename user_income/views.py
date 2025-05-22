from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages

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
        messages.success(request, 'Income successfully added.')

        return redirect('income')
