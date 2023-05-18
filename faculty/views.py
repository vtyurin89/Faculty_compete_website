from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import *
from .forms import *
from .models import *

# Create your views here.

@login_required
def index(request):
    context = {'title': 'Main page'}
    return render(request, 'faculty/index.html', context)


def login_teacher(request):
    if request.method == "POST":
        form = LoginTeacherForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
        context = {'title': 'Login', 'form': form}
        return render(request, 'faculty/login.html', context)
    else:
        form = LoginTeacherForm()
        context = {'title': 'Login', 'form': form}
        return render(request, 'faculty/login.html', context)


def logout_teacher(request):
    logout(request)
    return redirect('login')


def register_teacher(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        form = RegisterTeacherForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('index')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    form = RegisterTeacherForm()
    context = {'title': 'Register', 'form': form}
    return render(request, 'faculty/register.html', context)


@login_required
def create_school(request):
    if request.method == "POST":
        form = CreateSchoolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "School successfully created.")
            return redirect('index')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    form = CreateSchoolForm()
    context = {'title': 'Create School', 'form': form}
    return render(request, 'faculty/create_school.html', context)


@login_required
def join_school(request):
    if request.method == 'POST':
        school_code = request.POST['search']
        if school_code:
            try:
                school_match = School.objects.get(secret_key=school_code)
                if school_match.is_activated:
                    request.user.school_id = school_match.pk
                    request.user.save()
                    return redirect('index')
                else:
                    error_message = 'Sorry, cannot join this school because its faculties are not configured yet...'
                    context = {'menu': menu, 'title': 'Join school', 'error_message': error_message}
                    return render(request, 'faculty/join_school.html', context)
            except:
                error_message = "The school with this code does not exist..."
                context = {'menu': menu, 'title': 'Join school', 'error_message': error_message}
                return render(request, 'faculty/join_school.html', context)
        else:
            error_message = "Seems that you forgot to type anything..."
            context = {'menu': menu, 'title': 'Join school', 'error_message': error_message}
            return render(request, 'faculty/join_school.html', context)
    context = {'title': 'Join school'}
    return render(request, 'faculty/join_school.html', context)


def faculties_configure(request):
    if request.method == 'POST':
        print(request.POST.getlist('faculty'))
    context = {'title': 'Configure faculties'}
    return render(request, 'faculty/faculties_configure.html', context)

