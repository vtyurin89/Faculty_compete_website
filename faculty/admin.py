from django.contrib import admin
from .models import *


# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username',)


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'city', 'about', 'creation_date', 'secret_key', 'is_activated')


class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'points')


class ActionAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'faculty', 'amount', 'action_type', 'timestamp',)


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Action, ActionAdmin)