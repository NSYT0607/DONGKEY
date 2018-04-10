from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.template.loader import render_to_string
from .forms import IncomeForm, ExpenditureForm, DateInputForm
from club.models import Club


def club_accounting(request, pk):
    club = Club.objects.get(pk=pk)
    income_form = IncomeForm(request.POST or None, prefix='income')
    expenditure_form = ExpenditureForm(request.POST or None, request.FILES or None, prefix='expd')
    dateinput_form = DateInputForm()
    income_all = club.accounting.income_set.all().order_by('income_at')
    expd_all = club.accounting.expenditure_set.all().order_by('expd_at')
    if request.method == "POST":
        if income_form.is_valid():
            income = income_form.save(commit=False)
            income.accounting = club.accounting
            income.save()
        elif expenditure_form.is_valid():
            expenditure = expenditure_form.save(commit=False)
            expenditure.accounting = club.accounting
            expenditure.save()
        return redirect(reverse('finance:club_accounting', kwargs={'pk': pk, }))
    ctx = {
            'club': club,
            'account_sum': club.accounting.account_sum,
            'income_part': income_all[:20],
            'expd_part': expd_all[:20],
            'income_form': income_form,
            'expenditure_form': expenditure_form,
            'dateinput_form': dateinput_form,
    }
    return render(request, 'finance/club_accounting.html', ctx)


def non_admin_club_accounting(request, pk):
    club = Club.objects.get(pk=pk)
    dateinput_form = DateInputForm()
    income_all = club.accounting.income_set.all().order_by('income_at')
    expd_all = club.accounting.expenditure_set.all().order_by('expd_at')

    ctx = {
            'club': club,
            'account_sum': club.accounting.account_sum,
            'income_part': income_all[:20],
            'expd_part': expd_all[:20],
            'dateinput_form': dateinput_form,
    }
    return render(request, 'finance/non_admin_club_accounting.html', ctx)


def search_by_date(request, pk):
    club = Club.objects.get(pk=pk)
    form = DateInputForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('month'):
            year = int(form.cleaned_data['year'])
            month = int(form.cleaned_data['month'])
            search_income = club.accounting.income_set.filter(
                income_at__year="{0}".format(year),
                income_at__month="{0}".format(month))
            search_expd = club.accounting.expenditure_set.filter(
                expd_at__year="{0}".format(year),
                expd_at__month="{0}".format(month))
            ctx = {
                'year': year,
                'month': month,
                'club': club,
                'account_sum': per_date_account_sum(search_income, search_expd),
                'income_sum': accounting_part_sum(search_income),
                'expd_sum': accounting_part_sum(search_expd),
                'income_part': search_income.order_by('income_at'),
                'expd_part': search_expd.order_by('expd_at'),
            }
            html = render_to_string('finance/search_by_date.html', ctx)
            return JsonResponse({'success': True, 'html': html})

        else:
            year = int(form.cleaned_data['year'])
            search_income = club.accounting.income_set.filter(
                income_at__year="{0}".format(year),
                )
            search_expd = club.accounting.expenditure_set.filter(
                expd_at__year="{0}".format(year),
                )
            ctx = {
                'year': year,
                'club': club,
                'income_sum': accounting_part_sum(search_income),
                'expd_sum': accounting_part_sum(search_expd),
                'account_sum': per_date_account_sum(search_income, search_expd),
                'income_part': search_income.order_by('income_at'),
                'expd_part': search_expd.order_by('expd_at'),
            }
            html = render_to_string('finance/search_by_date.html', ctx)
            return JsonResponse({'success': True, 'html': html})
    else:
        return JsonResponse({'success': False, 'status': 'form_invaild'})


def per_date_account_sum(income_set, expd_set):
    account_sum = 0
    for income in income_set.all():
        account_sum += income.amount
    for expd in expd_set.all():
        account_sum -= expd.amount
    return account_sum


def accounting_part_sum(accounting_part_set):
    accounting_part_sum = 0
    for accounting_part in accounting_part_set.all():
        accounting_part_sum += accounting_part.amount
    return accounting_part_sum
