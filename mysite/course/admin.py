from django.contrib import admin
from .models import (UserProfile,Category,Subcategory,Course,Lesson,Assignment,
                     Exam,Question,Option,Certificate,Review)
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin


@admin.register(UserProfile, Option, Review)
class ProductAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class SabCategoryInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Subcategory
    extra = 1

@admin.register(Category)
class ProductAdmin(TranslationAdmin):
    inlines = [SabCategoryInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
class ExamInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Exam
    extra = 1


class AssignmentInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Assignment
    extra = 1

class LessonInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Lesson
    extra = 1


@admin.register(Course)
class ProductAdmin(TranslationAdmin):
    inlines = [LessonInline, AssignmentInline, ExamInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
class QuestionInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Question
    extra = 1


@admin.register(Exam)
class ProductAdmin(TranslationAdmin):
    inlines = [QuestionInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(Certificate)
