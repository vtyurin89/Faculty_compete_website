from django.template.defaultfilters import slugify
from .models import *


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

