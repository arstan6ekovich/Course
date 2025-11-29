from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (UserProfile, Category, Subcategory,
Course, Lesson, Assignment, Exam,
Question, Option, Certificate, Review, AssignmentSubmission)
from .serializers import (UserProfileListSerializer, UserProfileDetailSerializer,
CategoryListSerializers, CategoryDetailSerializers,
SubCategoryListSerializers, SubCategoryDetailSerializers,
CourseListSerializers, CourseDetailSerializers, LessonSerializers, AssignmentSerializers,
ExamListSerializers, ExamDetailSerializers,QuestionSerializers, OptionSerializers,
CertificateSerializers, ReviewListSerializers, ReviewDetailSerializers,
AssignmentSubmissionSerializer, LoginSerializer, UserSerializer)
from .permissions import TeacherPermission, AdminPermission, StudentPermission, StudentOrTeacherOrAdminPermission
from rest_framework.permissions import IsAuthenticated
from .paginations import CoursePagination
from .filters import CourseFilter
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
    permission_classes = [IsAuthenticated, AdminPermission]


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated, AdminPermission]


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializers
    permission_classes = [IsAuthenticated, AdminPermission | TeacherPermission]


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializers
    permission_classes = [IsAuthenticated, AdminPermission | TeacherPermission]


class SubCategoryListAPIView(generics.ListAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubCategoryListSerializers
    permission_classes = [IsAuthenticated, AdminPermission | TeacherPermission]


class SubCategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubCategoryDetailSerializers
    permission_classes = [IsAuthenticated, AdminPermission | TeacherPermission]


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializers
    permission_classes = [IsAuthenticated, StudentPermission | TeacherPermission | AdminPermission]
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter


class CourseDetailAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializers
    permission_classes = [IsAuthenticated, StudentPermission | TeacherPermission | AdminPermission]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializers
    permission_classes = [IsAuthenticated, TeacherPermission | AdminPermission]


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializers
    permission_classes = [IsAuthenticated, TeacherPermission | AdminPermission]


class ExamListAPIView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamListSerializers
    permission_classes = [IsAuthenticated, StudentPermission | TeacherPermission | AdminPermission]


class ExamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamDetailSerializers
    permission_classes = [IsAuthenticated, TeacherPermission | AdminPermission]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializers
    permission_classes = [IsAuthenticated, TeacherPermission | AdminPermission]


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializers
    permission_classes = [IsAuthenticated, TeacherPermission | AdminPermission]


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializers
    permission_classes = [IsAuthenticated, StudentPermission | AdminPermission]


class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializers
    permission_classes = [IsAuthenticated, StudentPermission | AdminPermission]


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializers
    permission_classes = [IsAuthenticated, StudentPermission | AdminPermission]


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [StudentOrTeacherOrAdminPermission]

