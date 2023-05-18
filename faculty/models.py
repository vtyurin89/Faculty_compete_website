from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


# Create your models here.


class Teacher(AbstractUser):
    school = models.ForeignKey('School', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta(AbstractUser.Meta):
        pass


class Director(Teacher):
    pass

    class Meta:
        proxy = True


class School(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name of the school')
    country = CountryField(verbose_name='Country', blank_label="(select country)", blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name='City')
    about = models.TextField(blank=True, null=True, verbose_name='Additional information')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    secret_key = models.CharField(max_length=50, blank=True, null=True, verbose_name='Secret key')
    is_activated = models.BooleanField(default=False, verbose_name='Faculties configured')

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class House(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name


# class Action(models.Model):
#     teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
#     faculty = models.ForeignKey('House', on_delete=models.CASCADE)
#     grade = models.ForeignKey('Grade', on_delete=models.CASCADE)
#     change = models.IntegerField()
#     timestamp = models.DateTimeField()
#     comment = models.TextField(max_length=1000)
#
#     def __str__(self):
#         return '(%s) %d to %s' % (self.teacher, self.change, self.faculty)

