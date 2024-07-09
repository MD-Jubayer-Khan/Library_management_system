from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import FormView
from library.models import Transaction
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from library.forms import DepositForm
from library.models import UserProfile
from library.views import send_email


# Create your views here.

class Signup(FormView):
    template_name = 'signup.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'signup information incorrect')
        return super().form_invalid(form)
    
class User_login(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context


class User_logout(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


@login_required
def deposit_money(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user_profile.balance += amount
            user_profile.save()
            send_email(request.user, amount, "Deposit Message", "deposit_email.html")
            return redirect('profile')
    else:
        form = DepositForm()

    return render(request, 'deposit_money.html', {'form': form})

@login_required
def profile(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'profile.html', {'transactions': transactions})



