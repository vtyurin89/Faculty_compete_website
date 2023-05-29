from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField

from .validators import *

# Create your models here.


def user_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'images/user_{0}/{1}'.format(instance.username, filename)


class Teacher(AbstractUser):
    school = models.ForeignKey('School', blank=True, null=True, on_delete=models.SET_NULL)
    teacher_image = models.ImageField(null=True, blank=True, upload_to=user_image_path, verbose_name='Profile image')

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

#slug generation functions in utils.py


class House(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, null=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.points < 0:
            self.points = 0
        return super().save(*args, **kwargs)


    class Meta:
        unique_together = ('school', 'name',)


class Action(models.Model):
    KINDS = (
        ('a', 'award'),
        ('b', 'deduct'),
    )
    teacher = models.ForeignKey('Teacher', blank=True, null=True, on_delete=models.CASCADE)
    faculty = models.ForeignKey('House', blank=True, null=True, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    action_type = models.CharField(max_length=1, choices=KINDS, default='a')
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=1000, blank=True, null=True,)

    def __str__(self):
        if self.action_type == 'a':
            return '{} awarded {} points to {}.'.format(self.teacher, self.amount, self.faculty)
        else:
            return '{} deducted {} points from {}.'.format(self.teacher, self.amount, self.faculty)


    def my_profile_action(self):
        if self.action_type == 'a':
            return 'You awarded {} points to {}.'.format(self.amount, self.faculty)
        else:
            return 'You deducted {} points from {}.'.format(self.amount, self.faculty)
