from pathlib import Path

from django.template.defaultfilters import slugify
from django_cleanup.signals import cleanup_post_delete, cleanup_pre_delete
from easy_thumbnails.files import get_thumbnailer

from .models import *
import os


#sidebar in account settings
profile_sidebar = [{'title': "User profile", 'url_name': 'profile_main_data', 'sidebar_pos': 1},
                   {'title': "School information", 'url_name': 'profile_user_school', 'sidebar_pos': 2},
                   {'title': "Recent actions", 'url_name': 'profile_recent_actions', 'sidebar_pos': 3},
                   {'title': "Safety", 'url_name': 'profile_change_password', 'sidebar_pos': 4},
]


#slug generation
def translate_cyrillic_slug(faculty, school):
    translated_faculty = faculty.translate(
        str.maketrans(
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
            "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"))
    translated_school = school.translate(
        str.maketrans(
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
            "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"))
    return translated_faculty, translated_school


def create_unique_slug(faculty, school):
    translated_faculty, translated_school = translate_cyrillic_slug(faculty, school)
    new_slug = f'{slugify(translated_school)}_{slugify(translated_faculty)}'
    check_slug = House.objects.filter(slug=new_slug)
    if check_slug.exists():
        new_slug = f"{new_slug}_{check_slug.count() + 1}"
    return new_slug


def thumbnail_auto_delete(**kwargs):
    teacher_instance = kwargs['instance']
    print(teacher_instance)
    teacher_instance.teacher_image.delete_thumbnails()

cleanup_pre_delete.connect(thumbnail_auto_delete)
