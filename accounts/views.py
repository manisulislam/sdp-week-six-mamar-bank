from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm
from django.contrib.auth import login

# Create your views here.

class UserRegistrationView(FormView):
    template_name='user_registration.html'
    form_class=UserRegistrationForm
    success_url='register'
    
    def form_valid(self, form):
        user=form.save()
        login(self.request, user)
        return super().form_valid(form)
        
