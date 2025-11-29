from .models import (UserProfile, Category, Subcategory,
                     Course, Lesson, Assignment,
                     Exam, Question, Option,
                     Review)
from modeltranslation.translator import TranslationOptions,register

@register(UserProfile)
class UserProfileTranslationOptions(TranslationOptions):
    fields = ('role', 'bio')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Subcategory)
class SubcategoryTranslationOptions(TranslationOptions):
    fields = ('subcategory_name',)


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('course_name', 'description', 'level')


@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('lesson_title',)



@register(Assignment)
class AssignmentTranslationOptions(TranslationOptions):
    fields = ('assignment_title', 'description')


@register(Exam)
class ExamTranslationOptions(TranslationOptions):
    fields = ('exam_title',)


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('question_name',)


@register(Option)
class OptionTranslationOptions(TranslationOptions):
    fields = ('option_name',)


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)