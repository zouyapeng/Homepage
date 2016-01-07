# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login

from models import UserProfile


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100,
                               label='Username',
                               required=True,
                               widget=forms.TextInput(attrs={'class' : 'form-control',
                                                             'type': 'text',
                                                             'placeholder':'Username'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class' : 'form-control',
                                                            'type': 'text',
                                                            'placeholder':'Email',}))

    sex = forms.ChoiceField(label='Sex',
                            choices=(('Male','Male'),('Female','Female')),
                            widget=forms.RadioSelect())

    password = forms.CharField(max_length=100,
                               label='Password',
                               widget=forms.PasswordInput(attrs={'class' : 'form-control',
                                                                 'type': 'password',
                                                                 'placeholder':'Password'}))

    password_confirm = forms.CharField(max_length=100,
                               label='Password Confirm',
                               widget=forms.PasswordInput(attrs={'class' : 'form-control',
                                                                 'type': 'password',
                                                                 'placeholder':'Re-type Password'}))

    def clean(self):
        '''Required custom validation for the form.'''
        super(forms.Form,self).clean()
        if 'password' in self.cleaned_data and 'password_confirm' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
                self._errors['password'] = [u'Passwords must match.']
                self._errors['password_confirm'] = [u'Passwords must match.']
        return self.cleaned_data

    def save(self):
        form = self.cleaned_data
        user = User.objects.create(username = form['username'],
                                    email = form['email'])
        user.set_password(form['password'])
        user.save()
        userprofile = UserProfile.objects.create(user=user,
                                                 sex=form['sex'])
        userprofile.save()



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,
                               label='Username',
                               widget=forms.TextInput(attrs={'class' : 'form-control',
                                                             'type': 'text',
                                                             'placeholder':'Username'}))
    password = forms.CharField(max_length=100,
                               label='Password',
                               widget=forms.PasswordInput(attrs={'class' : 'form-control',
                                                                 'type': 'password',
                                                                 'placeholder':'Password'}))

    remember_me = forms.BooleanField(required=False ,widget=forms.CheckboxInput(attrs={'type':'checkbox',
                                                                                    'value':'remember-me'}))



