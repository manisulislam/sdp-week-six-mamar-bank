
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .forms import DepositForm, WithdrawForm, LoanForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Transaction
from .constants import DEPOSIT, WITHDRAWAL, LOAN, LOAN_PAID
from django. contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView
import datetime
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views import View
# Create your views here.

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name=''
    model=Transaction
    success_url=''
    title=''
    
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account,
        })
        return kwargs
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'title':self.title
        })
        
        
class DepositMoneyView(TransactionCreateMixin):
    form_class=DepositForm
    title='Deposit'
    
    def get_initial(self):
        initial={'transaction_type':DEPOSIT}
        return initial
    
    def form_valid(self, form):
        amount=form.cleaned_data['amount']
        account=self.request.user.account
        account.balance+=amount
        account.save(
            update_fields=['balance']
        )
        messages.success(self.request, f'{amount} $ deposited successfully')
        return super().form_valid(form)
        
class WithdrawMoneyView(TransactionCreateMixin):
    form_class=WithdrawForm
    title='Withdraw Money'
    
    def get_initial(self):
        initial={'transaction_type':WITHDRAWAL}
        return initial
    
    def form_valid(self, form):
        amount=form.cleaned_data['amount']
        account=self.request.user.account
        account.balance-=amount
        account.save(
            update_fields=['balance']
        )
        messages.success(self.request, f'{amount} $ withdraw successfully')
        return super().form_valid(form)
        
class LoanMoneyView(TransactionCreateMixin):
    form_class=LoanForm
    title='Request for loan'
    
    def get_initial(self):
        initial={'transaction_type':LOAN}
        return initial
    
    def form_valid(self, form):
        amount=form.cleaned_data['amount']
        current_loan_count=Transaction.objects.filter(account=self.request.user.account, transaction_type=LOAN, loan_approve=True).count()
        if current_loan_count>=3:
            return HttpResponse("you exceed loan limits ")
        messages.success(self.request, f'your loan {amount} $ successfully sent to be admin ')
        return super().form_valid(form)
        

class TransactionReportView(LoginRequiredMixin,ListView):
    template_name=''
    model=Transaction
    balance=0
    
    def get_queryset(self) :
        queryset=super().get_queryset().filter(account=self.request.user.account)
        start_date_str=self.request.GET.get('start_date')
        end_date_str=self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date=datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date=datetime.strptime(end_date_str, '%Y-%m-%d').date()
            queryset=queryset.filter(timestamp__date_gte=start_date, timestamp__date_lte=end_date)
            self.balance=Transaction.objects.filter(timestamp__date_gte=start_date, timestamp__date_lte=end_date).aggregate(Sum('amount'))['amount_sum']
        else:
            self.balance=self.request.user.account.balance
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'account':self.request.user.account,
        })
        return context
        

class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan=get_object_or_404(Transaction, id=loan_id)
        if loan.loan_approve:
            user_account=loan.account
            if loan.amount<=user_account.balance:
                user_account.balance-=loan.amount
                loan.balance_after_transaction=user_account.balance
                user_account.save()
                loan.transaction_type=LOAN_PAID
                loan.save()
                return redirect()
            else:
                messages.error(request, 'insufficient balance')
                return redirect()


class LoanListView(LoginRequiredMixin, ListView):
    template_name=''
    model=Transaction
    context_object_name='loan_list'
    def get_queryset(self):
        queryset=super().get_queryset().filter(account=self.request.user.account, transaction_type=LOAN)
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'account':self.request.user.account,
        })
        return context