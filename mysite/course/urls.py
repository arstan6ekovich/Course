from rest_framework import routers
from django.urls import path, include
from .views import (UserProfileListAPIView, UserProfileDetailAPIView,
                    CategoryListAPIView, CategoryDetailAPIView,
                    SubCategoryListAPIView, SubCategoryDetailAPIView,
                    CourseListAPIView, CourseDetailAPIView, LessonViewSet, AssignmentViewSet,
                    ExamListAPIView, ExamDetailAPIView, QuestionViewSet, OptionViewSet,
                    CertificateViewSet, ReviewListAPIView, ReviewDetailAPIView,
                    AssignmentSubmissionViewSet, CustomLoginView, RegisterView, LogoutView)


router = routers.SimpleRouter()

router.register(r'lessons', LessonViewSet, basename='lessons_list')
router.register(r'assignment', AssignmentViewSet, basename='assignment_list')
router.register(r'assignment_submission', AssignmentSubmissionViewSet, 'assignment_submission_list')
router.register(r'question', QuestionViewSet, 'question_list')
router.register(r'option', OptionViewSet, 'optionList')
router.register(r'certificate', CertificateViewSet, basename='certificate_list')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/users/', UserProfileListAPIView.as_view(), name='user_list'),
    path('auth/users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('subcategory/', SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('subcategory/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory_detail'),
    path('course/', CourseListAPIView.as_view(), name='course_list'),
    path('course/<int:pk>/', CourseDetailAPIView.as_view(), name='course_detail'),
    path('reviews/', ReviewListAPIView.as_view(), name='reviews_list'),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='reviews_detail'),
    path('exam/', ExamListAPIView.as_view(), name='exam_list'),
    path('exam/<int:pk>/', ExamDetailAPIView.as_view(), name='exam_detail'),
]