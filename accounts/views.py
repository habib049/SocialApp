from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages, auth
from django.urls import reverse_lazy

from .forms import RegistrationForm, LoginForm
from django.views.generic import CreateView, FormView, RedirectView
from .models import User


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'accounts/register.html'

    def post(self, request, *args, **kwargs):
        new_user = RegistrationForm(request.POST)
        if new_user.is_valid():
            new_user.save()
            return redirect('accounts:user_login')
        return render(request, 'accounts/register.html', {'form': new_user})


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    url = reverse_lazy('accounts:user_login')

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)
