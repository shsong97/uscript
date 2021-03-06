# -*- coding: utf-8 -*-
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _


class RegistrationForm(forms.Form):
    username = forms.CharField(label='ID', max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'ID'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Your email'}))
    first_name = forms.CharField(label='First Name', max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(label='Last Name', max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Password(confirm)',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )
    
    # clean_<field> : valid field

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Incorrect password')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'\w+$', username):
            raise forms.ValidationError(
                'user name allows alphabet, number, underground.')

        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('alread exists.')


class UploadFileForm(forms.Form):
    file = forms.FileField()
