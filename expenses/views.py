from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Expense
from django.core import paginator


# Create your views here.

@login_required(login_url='authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
    }
    return render(request, 'expenses/index.html', context)

def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':

        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Please enter amount.')
            return render(request, 'expenses/add_expense.html', context)

        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description cannot be empty.')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user ,amount=amount, description=description, date=date, category=category)
        messages.success(request, 'Expense successfully added.')

        return redirect('expenses')

def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories,
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Please enter amount.')
            return render(request, 'expenses/edit-expense.html', context)

        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description cannot be empty.')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount=amount
        expense.description=description
        expense.date=date
        expense.category=category
        expense.save()
        messages.success(request, 'Expense successfully updated.')

        return redirect('expenses')

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense successfully deleted.')
    return redirect('expenses')