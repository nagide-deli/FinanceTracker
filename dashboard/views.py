import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ContactForm
from .models import Income, Expense, Budget, ContactMessage
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth import logout


@login_required
def dashboard(request):
    user = request.user

    if request.method == 'POST':
        if 'add_income' in request.POST:  # Handling Add Income form
            amount = request.POST.get('amount')
            source = request.POST.get('source')
            date = request.POST.get('date')

            # Validate input
            if not amount or not source:
                messages.error(request, 'Amount and Source are required to add income.')
            else:
                Income.objects.create(
                    user=user,
                    amount=amount,
                    source=source,
                    date=date,
                )
                messages.success(request, 'Income added successfully!')
            return redirect('dashboard')

        if 'add_expense' in request.POST:  # Handling Add Expense form
            amount = request.POST.get('amount')
            category = request.POST.get('category')
            date = request.POST.get('date')

            # Validate input
            if not amount or not category:
                messages.error(request, 'Amount and Category are required to add expense.')
            else:
                Expense.objects.create(
                    user=user,
                    amount=amount,
                    category=category,
                    date=date,
                )
                messages.success(request, 'Expense added successfully!')
            return redirect('dashboard')

        if 'budget' in request.POST:
            monthly_limit = request.POST.get('monthly_limit')
            if not monthly_limit:
                messages.error(request, 'Monthly limit is required')
            else:
                budget, created = Budget.objects.get_or_create(user=user)
                budget.monthly_limit = monthly_limit
                budget.balance = budget.total_income - float(monthly_limit)
                budget.save()
                messages.success(request, 'Budget updated successfully!')
            return redirect('dashboard')

    # Fetch data
    total_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    # Fetch expenses by category
    expenses_by_category = (
        Expense.objects.filter(user=user)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    # Fetch budget
    budget = Budget.objects.filter(user=user).first()

    # Fetch data for reports
    monthly_income = list(
        Income.objects.filter(user=user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    monthly_expense = list(
        Expense.objects.filter(user=user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    # Serialize data to JSON
    monthly_income_json = json.dumps(monthly_income, cls=DjangoJSONEncoder)
    monthly_expense_json = json.dumps(monthly_expense, cls=DjangoJSONEncoder)
    # expenses_by_category_json = json.dumps(list(expenses_by_category), cls=DjangoJSONEncoder)

    # Pass data to template
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'budget': budget,
        'monthly_income_json': list(monthly_income_json),
        'monthly_expense_json':list (monthly_expense_json),
        'expenses_by_category':list (expenses_by_category),
    }
    return render(request, 'dashboard.html', context)


def user_logout(request):
    """
    Logs out the user and redirects to the landing page.
    """
    logout(request)
    return redirect('landingpage')


def landingpage(request):
    return render(request, 'landingpage.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database (optional)
            ContactMessage.objects.create(**form.cleaned_data)

            # Send a success message
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_us')  # Replace with your URL name
    else:
        form = ContactForm()

    return render(request, 'contactus.html', {'form': form})
