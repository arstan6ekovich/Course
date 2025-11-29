import django_filters
from .models import Course

class CourseFilter(django_filters.FilterSet):
    course_name = django_filters.CharFilter(lookup_expr='icontains')

    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    level = django_filters.ChoiceFilter(choices=Course.LEVEL_CHOICES)

    premium_type = django_filters.BooleanFilter()

    created_at = django_filters.DateFromToRangeFilter()

class Meta:
    model = Course
    fields = [
        'course_name',
        'price_min', 'price_max',
        'level',
        'premium_type',
        'created_at',
    ]
