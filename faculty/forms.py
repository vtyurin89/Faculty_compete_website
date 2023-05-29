from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django_countries.widgets import CountrySelectWidget

from random import choice
import string

from .models import *


def generate_secret_code():
    sequence_for_code_generation = string.ascii_lowercase + string.ascii_uppercase
    secret_key = ''.join(choice(sequence_for_code_generation) for i in range(12))
    return secret_key


class RegisterTeacherForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat password'}))

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Password mismatch', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        teacher = super(RegisterTeacherForm, self).save(commit=False)
        teacher.email = self.cleaned_data['email']
        if commit:
            teacher.save()
        return teacher

    class Meta:
        model = Teacher
        fields = ('username', 'email', 'password1', 'password2')


class LoginTeacherForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login', 'name': 'username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'name': 'password'}))


class CreateSchoolForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop("user_id", None)
        super(CreateSchoolForm, self).__init__(*args, **kwargs)

    class Meta:
        model = School
        fields = ["name", "country", "city", "about"]
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'name': 'name'}),
                   'country': CountrySelectWidget(attrs={'class': 'form-control', 'name': 'country'}),
                   'city': forms.TextInput(attrs={'class': 'form-control', 'name': 'city'}),
                   'about': forms.Textarea(attrs={'class': 'form-control', 'name': 'about', 'placeholder': 'Something interesting about your school?..'})}

    def save(self, commit=True, **kwargs):
        my_form_object = super(CreateSchoolForm, self).save(commit=False)
        while True:
            new_secret_key = generate_secret_code()
            check_secret_key = School.objects.filter(secret_key=new_secret_key)
            if check_secret_key.exists():
                pass
            else:
                my_form_object.secret_key = new_secret_key
                break
        if commit:
            my_form_object.save()
        Teacher.objects.filter(pk=self.user_id).update(school_id=my_form_object.pk)
        return my_form_object


class CreateHouseForm(ModelForm):

    class Meta:
        model = House
        fields = ["name",]
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'name': 'name'}),}


class ProfileChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='New password', max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Repeat password', max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ProfileConfigureTeacher(ModelForm):
    first_name = forms.CharField(label='First name', max_length=255, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name'}))
    last_name = forms.CharField(label='Last name', max_length=255, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name'}))
    email = forms.EmailField(label='Email', required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'name': 'email'}))
    teacher_image = forms.ImageField(label='Profile picture', required=False,
                             widget=forms.FileInput(attrs={'class': 'form-control', 'name': 'teacher_image'}))


    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'email', 'teacher_image')

