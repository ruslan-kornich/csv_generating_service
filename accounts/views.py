from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from .forms import LoginForm


class LoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    error = 'Your account is not active.'
            else:
                error = 'Invalid username or password'
        else:
            error = form.errors
        return render(request, self.template_name, {'form': form, 'error': error})


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')
