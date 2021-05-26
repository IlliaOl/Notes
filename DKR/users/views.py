from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CreateCustomUserForm


class SignUp(CreateView):
	form_class = CreateCustomUserForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'
