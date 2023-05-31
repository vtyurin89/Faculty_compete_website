from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Max, Q
from django.core.paginator import Paginator
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
        if new_action_amount and int(new_action_amount) > 50000:
            messages.error(request, 'Sorry, cannot award or deduct THAT many points')
        elif new_action_amount and int(new_action_amount) > 0:
            new_action_record = Action.objects.create(
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
            messages.success(request, f"{new_action_record.my_profile_action()}")
        return redirect('index')
    else:
        if request.user.school and request.user.school.is_activated:
            latest_action_list = Action.objects.filter(faculty__school=request.user.school).order_by('-id')[:10]
            winning_house = House.objects.filter(Q(school=request.user.school) & Q(points__gte=House.objects.filter(school=request.user.school).aggregate(Max('points')).get('points__max')))
            our_houses = House.objects.filter(school=request.user.school).order_by('-points')
            house_scores = [house.points for house in our_houses]
            house_names = [house.name for house in our_houses]
        else:
            latest_action_list = None
            winning_house = None
            house_scores = None
            house_names = None
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
        print(request)
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
    current_teacher_user = Teacher.objects.get(pk=request.user.id)

    if request.method == "POST":
        form = ProfileConfigureTeacher(request.POST, request.FILES, instance=current_teacher_user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, current_teacher_user)
            messages.success(request, "Profile updated.")
            return redirect('profile_main_data')
    form = ProfileConfigureTeacher(instance=current_teacher_user)
    context = {'title': 'Account settings',
               'form': form,
               'profile_sidebar': profile_sidebar,
               'context_sidebar_pos': 1}
    return render(request, 'faculty/profile_main_data.html', context)


@login_required
def profile_user_school(request):
    if request.user.school:
        my_school = School.objects.filter(pk=request.user.school_id)[0]
        my_school_faculties = House.objects.filter(school=my_school)
    else:
        my_school = None
        my_school_faculties = None
    context = {'title': 'School information',
               'my_school': my_school,
               'my_school_faculties': my_school_faculties,
               'profile_sidebar': profile_sidebar,
               'context_sidebar_pos': 2}
    return render(request, 'faculty/profile_user_school.html', context)


@login_required
def profile_recent_actions(request):
    user_action_list = Action.objects.filter(Q(teacher=request.user) & Q(faculty__school=request.user.school)).order_by('-id')

    pagination_range = 15
    paginator = Paginator(user_action_list, pagination_range)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'title': 'Your recent actions',
               'user_action_list': user_action_list,
               'profile_sidebar': profile_sidebar,
               'context_sidebar_pos': 3,
               'page_obj': page_obj}
    return render(request, 'faculty/profile_recent_actions.html', context)


@login_required
def profile_change_password(request):
    if request.method == 'POST':
        form = ProfileChangePassword(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed")
            return redirect('profile_change_password')
    else:
        form = ProfileChangePassword(user=request.user)
        context = {'title': 'Change password',
               'profile_sidebar': profile_sidebar,
               'form': form,
               'context_sidebar_pos': 4}
        return render(request, 'faculty/profile_change_password.html', context)
