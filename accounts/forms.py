from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE, GENDER_TYPE
from .models import UserAddress, UserBankAccount

class UserRegistrationForm(UserCreationForm):
    account_type=forms.ChoiceField(choices=ACCOUNT_TYPE)
    gender_type=forms.ChoiceField( choices=GENDER_TYPE)
    birth_date=forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    postal_code=forms.IntegerField()
    country=forms.CharField(max_length=100)
    
    class Meta():
        model=User
        fields=['username', 'first_name','last_name','email','password1','password2','account_type', 'gender_type','birth_date','street_address','city','postal_code','country']
        
    def save(self, commit=True):
        our_user=super().save(commit=False)
        
        if commit==True:
            our_user.save()
            account_type=self.changed_data.get('account_type')
            gender_type=self.cleaned_data.get('gender_type')
            birth_date=self.cleaned_data.get('birth_date')
            street_address=self.cleaned_data.get('street_address')
            city=self.cleaned_data.get('city')
            postal_code=self.cleaned_data.get('postal_code')
            country=self.cleaned_data.get('country')
            
            UserBankAccount.objects.create(
                user=our_user,
                account_type=account_type,
                gender_type=gender_type,
                birth_date=birth_date,
                account_no=100000+our_user.id
            )
            
            UserAddress.objects.create(
                user=our_user,
                street_address=street_address,
                city=city,
                postal_code=postal_code,
                country=country
            )
        return our_user