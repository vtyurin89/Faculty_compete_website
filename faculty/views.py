from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Max, Q
from .utils import *
from .forms import *
from .models import *

# Create your views here.


@login_required
def index(request):
    faculty_list = House.objects.filter(school=request.user.school)
    if request.method == 'POST':
        for faculty in faculty_list:
            if faculty.slug in request.POST and 'award' in request.POST:
                new_action_faculty = faculty
                new_action_type = 'a'
                break
            elif faculty.slug in request.POST and 'deduct' in request.POST:
                new_action_faculty = faculty
                new_action_type = 'b'
                break
        new_action_amount = request.POST[new_action_faculty.slug]
        if new_action_amount and int(new_action_amount) > 500000:
            messages.error(request, 'Sorry, cannot award or deduct THAT many points')
        elif new_action_amount and int(new_action_amount) > 0:
            Action.objects.create(
                faculty=new_action_faculty,
                teacher=request.user,
                amount=new_action_amount,
                action_type=new_action_type,
                )
            house_makechange = House.objects.get(pk=new_action_faculty.pk)
            if new_action_type == 'a':
                house_makechange.points = house_makechange.points + int(new_action_amount)
            else:
                house_makechange.points = house_makechange.points - int(new_action_amount)
            house_makechange.save()
        return redirect('index')
    else:
        latest_action_list = Action.objects.filter(faculty__school=request.user.school).order_by('-id')[:10]
        winning_house = House.objects.filter(Q(school=request.user.school.pk) & Q(points__gte=House.objects.aggregate(Max('points')).get('points__max')))
        our_houses = House.objects.filter(school=request.user.school.pk).order_by('-points')
        house_scores = [house.points for house in our_houses]
        house_names = [house.name for house in our_houses]
        context = {'title': 'Main page',
                   'faculty_list': faculty_list,
                   'action_list': latest_action_list,
                   'winning_house': winning_house,
                   'house_scores': house_scores,
                   'house_names': house_names,
                   }
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
        user_id = request.user.id
        form = CreateSchoolForm(request.POST, user_id=request.user.id)
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
                    context = {'title': 'Join school', 'error_message': error_message}
                    return render(request, 'faculty/join_school.html', context)
            except:
                error_message = "The school with this code does not exist..."
                context = {'title': 'Join school', 'error_message': error_message}
                return render(request, 'faculty/join_school.html', context)
        else:
            error_message = "Seems that you forgot to type anything..."
            context = {'title': 'Join school', 'error_message': error_message}
            return render(request, 'faculty/join_school.html', context)
    context = {'title': 'Join school'}
    return render(request, 'faculty/join_school.html', context)


@login_required()
def faculties_configure(request):
    if request.method == 'POST':
        raw_list = request.POST.getlist('faculty')
        faculty_list = list(filter(lambda x: x != "", raw_list))
        if faculty_list:
            for faculty in faculty_list:
                school = request.user.school.name
                faculty_slug = create_unique_slug(faculty, school)
                House.objects.get_or_create(
                    name=faculty,
                    school=request.user.school,
                    slug=faculty_slug,
                )
            School.objects.filter(pk=request.user.school_id).update(is_activated=True)
            messages.success(request, "Houses successfully created.")
            return redirect('index')
        else:
            context = {'title': 'Configure faculties'}
            messages.error(request, 'Please choose the names of the faculties.')
            return render(request, 'faculty/faculties_configure.html', context)
    context = {'title': 'Configure faculties'}
    return render(request, 'faculty/faculties_configure.html', context)

@login_required
def profile_main_data(request):
    context = {'title': 'Account information'}
    return render(request, 'faculty/profile_main_data.html', context)
