# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.encoding import force_text
from django.views.generic import FormView, RedirectView
from accounts.forms import LoginForm,RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.forms.utils import ErrorList

# Create your views here.
class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy("blog:index")

    def get(self, request, *args, **kwargs):
        self.initial= {
            'sex':'Male'
        }

        return super(RegistrationView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                User.objects.get(username=username)
                errors = form._errors.setdefault("username", ErrorList())
                errors.append(u"username had be used!")
                return self.form_invalid(form)
            except ObjectDoesNotExist:
                pass

            try:
                User.objects.get(email=email)
                errors = form._errors.setdefault("email", ErrorList())
                errors.append(u"email had be used!")
                return self.form_invalid(form)
            except ObjectDoesNotExist:
                pass

            form.save()

            user = authenticate(username=username, password=password)
            if user:
                login(self.request,user)

        return  super(RegistrationView, self).post(request, *args, **kwargs)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy("blog:index")

    def post(self, request, *args, **kwargs):
        # redirect_to = request.GET['next']
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(username = username, password = password)
            if user:
                login(self.request, user)
                if not remember_me:
                    request.session.set_expiry(0)
            else:
                errors = form._errors.setdefault("password", ErrorList())
                errors.append(u"username or password is incorrect!")
                return self.render_to_response(self.get_context_data(form=form))

            # if redirect_to:
            #     return HttpResponseRedirect(redirect_to)
            return self.form_valid(form)
            # return HttpResponseRedirect(force_text(reverse_lazy('blog:index')))
        else:
            return self.form_invalid(form)

class LogoutView(RedirectView):
    permanent = True
    url = reverse_lazy("blog:index")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)





