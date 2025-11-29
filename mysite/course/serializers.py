from .models import (UserProfile,Category,Subcategory,Course,Lesson,Assignment,
                     AssignmentSubmission,Exam,Question,Option,Certificate,Review)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'role', 'profile_picture', 'bio')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileNameSerializer (serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'role', 'profile_picture')


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileListSerializer (serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'profile_picture', 'email', 'role')


class UserProfileDetailSerializer (serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    last_login = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'is_superuser', 'username', 'last_login',
                  'email', 'is_staff', 'is_active', 'date_joined', 'role',
                  'profile_picture', 'bio', 'groups', 'user_permissions')


class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name')


class CategoryNameSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_name',)


class SubCategoryDetailSerializers(serializers.ModelSerializer):
    category = CategoryNameSerializers()

    class Meta:
        model = Subcategory
        fields = ('id', 'subcategory_name', 'category')


class SubCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'subcategory_name')


class CategoryDetailSerializers(serializers.ModelSerializer):
    subcategories = SubCategoryListSerializers(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('category_name', 'subcategories')



class ReviewListSerializers(serializers.ModelSerializer):
    user = UserProfileNameSerializer()
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%m'))

    class Meta:
        model = Review
        fields = ('id', 'user', 'rating', 'comment', 'created_at')


class ReviewDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CourseNameSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('course_name', 'level')


class LessonSerializers(serializers.ModelSerializer):
    course = CourseNameSerializers()

    class Meta:
        model = Lesson
        fields = ('id', 'lesson_title', 'video_url', 'content', 'course')


class CourseListSerializers(serializers.ModelSerializer):
    created_by = UserProfileNameSerializer()
    get_discount_price = serializers.ModelSerializer()
    get_avg_reviews = serializers.ModelSerializer()
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    updated_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))

    class Meta:
        model = Course
        fields = ('id', 'course_image', 'course_name',
                  'description', 'price', 'get_discount_price',
                  'created_by', 'premium_type', 'bestseller_type',
                  'get_avg_reviews', 'created_at', 'updated_at')

    def get_discount_price (self, object):
        return self.get_discount_price.object()

    def get_avg_reviews(self, object):
        return self.get_avg_reviews.object()


class CourseDetailSerializers(serializers.ModelSerializer):
    created_by = UserProfileNameSerializer()
    get_discount_price = serializers.ModelSerializer()
    get_avg_reviews = serializers.ModelSerializer()
    subcategory = SubCategoryListSerializers()
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    updated_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    get_count_reviews = serializers.ModelSerializer()
    reviews = ReviewListSerializers(many=True, read_only=True)
    lessons = LessonSerializers(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'course_image', 'subcategory', 'course_name',
                  'description', 'level', 'price', 'premium_type',
                  'bestseller_type', 'created_by', 'created_at',
                  'updated_at', 'get_discount_price', 'get_avg_reviews',
                  'get_count_reviews', 'reviews', 'lessons')


    def get_discount_price (self, object):
        return self.get_discount_price.object()

    def get_avg_reviews(self, object):
        return self.get_avg_reviews.object()

    def get_count_reviews (self, object):
        return self.get_count_reviews.object()




class AssignmentSerializers(serializers.ModelSerializer):
    due_date = serializers.DateField(format='%d-%m-%Y')
    course = CourseNameSerializers()

    class Meta:
        model = Assignment
        fields = ('id', 'course', 'assignment_title', 'description', 'due_date')


class AssignmentSubmissionSerializer (serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'


class ExamListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ('id', 'exam_title', 'duration', 'passing_score')


class ExamDetailSerializers(serializers.ModelSerializer):
    course = CourseNameSerializers()

    class Meta:
        model = Exam
        fields = ('course', 'exam_title', 'duration', 'passing_score')


class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class OptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class CertificateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'

