from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, \
    YearPickerInput

from django.contrib.auth import authenticate, login
from django.forms import Form, widgets
from django import forms
from django.shortcuts import redirect, render

from app.models.category import Category
from app.models.person import Person
from app.models.question import Question
from app.models.tag import Tag


class DateInput(forms.DateInput):
    input_type = 'date'


class FormRegister(Form):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'birth', 'email', 'password_1', 'password_2', 'hobby', 'personality', 'way_of_life',)


    first_name = forms.CharField(label='first_name', max_length=200, min_length=4,
                                 widget=forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                               'placeholder': 'First Name'}))
    last_name = forms.CharField(label='last_name', max_length=200, min_length=4,
                                widget=forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                              'placeholder': 'Last Name'}))

    # birth = forms.DateField(widget=DateInput)

    birth = forms.DateField(
        label='birth',
        widget=DatePickerInput(format='%m/%d/%Y')
    )

    email = forms.CharField(label='email', max_length=200, min_length=4,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                          'placeholder': 'Email'}))
    password_1 = forms.CharField(label='password_1', max_length=200, min_length=4,
                                 widget=widgets.PasswordInput(attrs={'placeholder': 'Password',
                                                                     'class': 'form-control form-control-user'}))
    password_2 = forms.CharField(label='password_2', max_length=200, min_length=4,
                                 widget=widgets.PasswordInput(attrs={'placeholder': 'Password',
                                                                     'class': 'form-control form-control-user'}))
    # avatar = forms.FileField(label='avatar', widget=widgets.FileInput(attrs={'class': ''}))

    hobby = forms.ModelChoiceField(
        queryset=Tag.objects.filter(categories__description='hobby'),
        widget=forms.Select(attrs={'class': 'form-control form-control-user'}),
        required=False,
    )
    personality = forms.ModelChoiceField(
        queryset=Tag.objects.filter(categories__description='personality'),
        widget=forms.Select(attrs={'class': 'form-control form-control-user'}),
        required=False,
    )
    way_of_life = forms.ModelChoiceField(
        queryset=Tag.objects.filter(categories__description='way_of_life'),
        widget=forms.Select(attrs={'class': 'form-control form-control-user'}),
        required=False,
    )



    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        first_name.replace(" ", "")
        first_name.replace(",", "")
        if not first_name.isalpha():
            self.add_error('first_name', 'Seulement que des lettres')
            return None
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        last_name.replace(" ", "")
        last_name.replace(",", "")
        if not last_name.isalpha():
            self.add_error('last_name', 'Seulement que des lettres')
            return None
        return self.cleaned_data['last_name']

    def clean(self):
        password_1 = self.cleaned_data.get('password_1')
        password_2 = self.cleaned_data.get('password_2')
        if password_1 != password_2:
            self.add_error('password_1', 'Les mots de passe sont différent')
