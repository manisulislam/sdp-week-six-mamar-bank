from django.db import models
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE, GENDER_TYPE

# Create your models here.
class UserBankAccount(models.Model):
    user=models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_no=models.IntegerField(unique=True)
    account_type=models.CharField(max_length=20, choices=ACCOUNT_TYPE)
    gender=models.CharField(max_length=10, choices=GENDER_TYPE)
    birth_date=models.DateField(null=True, blank=True)
    balance=models.DecimalField(default=0,max_digits=12,decimal_places=2)
    initial_deposit_date=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.account_no
    
class UserAddress(models.Model):
    user=models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    postal_code=models.IntegerField()
    country=models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.user.email
    
    