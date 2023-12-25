from .models import Transaction
from django import forms
from django.db import transaction

class TransactionForm(forms.ModelForm):
    class Meta():
        model=Transaction
        fields=['account', 'transaction_type']
        
    def __init__(self, *args, **kwargs):
        self.account=kwargs.pop('account')
        super.__init__(*args,**kwargs)
        self.fields['transaction_type'].disabled=True
        self.fields['transaction_type'].widget=forms.HiddenInput
        
    def save(self, commit=True):
        self.instance.account=self.account
        self.instance.balance_after_transaction=self.account.balance
        return super().save()


class DepositForm(Transaction):
    def clean_amount(self):
        min_deposit_amount=100
        amount=self.cleaned_data['amount']
        if amount < min_deposit_amount:
            raise forms.ValidationError(f'Minimum deposit amount is {min_deposit_amount}$')
        return amount
    
class WithdrawForm(Transaction):
    def clean_amount(self):
        acount=self.account
        min_withdraw_amount=500
        max_withdraw_amount=20000
        amount=self.cleaned_data['amount']
        if amount < min_withdraw_amount:
            raise forms.ValidationError(f'Minimum withdraw amount is {min_withdraw_amount}$')
        
        if amount>max_withdraw_amount:
            raise forms.ValidationError(f'Maximum withdraw amount is {max_withdraw_amount}$')
        if amount>acount.balance:
            raise forms.ValidationError(f'Insufficient balance')
        return amount
    
class LoanForm(Transaction):
    def clean_amount(self):
        amount=self.cleaned_data['amount']
       
        return amount