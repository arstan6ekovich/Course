from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('admin', 'Администратор'),
    )

    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='student')
    profile_picture = models.ImageField(upload_to='user_profile/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"



class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    subcategory_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.subcategory_name


class Course(models.Model):
    course_image = models.ImageField(upload_to='course_image/', null=True, blank=True)
    LEVEL_CHOICES = (
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    )

    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="courses")
    course_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    level = models.CharField(max_length=16, choices=LEVEL_CHOICES)
    price = models.PositiveSmallIntegerField()
    premium_type = models.BooleanField(default=False)
    bestseller_type = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="created_courses"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    DISCOUNT_PERCENT = Decimal('0.85')

    def get_discount_price(self):
        if not self.price:
            return None
        discount_amount = self.price * self.DISCOUNT_PERCENT
        new_price = self.price - discount_amount
        return new_price.quantize(Decimal('0.01'))

    def get_avg_reviews(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum([i.rating for i in ratings]) / ratings.count(), 1)
        return 0

    def get_count_reviews(self):
        return self.reviews.all().count()




    def __str__(self):
        return f"{self.course_name} ({self.get_level_display()})"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    lesson_title = models.CharField(max_length=150)
    video_url = models.URLField(null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.lesson_title


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    assignment_title = models.CharField(max_length=150)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return self.assignment_title


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    file = models.FileField(upload_to="assignments/", null=True, blank=True)
    answer_text = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.assignment.assignment_title}"


class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exams")
    exam_title = models.CharField(max_length=150)
    duration = models.DurationField()
    passing_score = models.PositiveIntegerField(default=60)

    def __str__(self):
        return self.exam_title


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    question_name = models.CharField(max_length=250)

    def __str__(self):
        return self.question_name


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    option_name = models.CharField(max_length=250)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_name


class Certificate(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_url = models.FileField(upload_to='certificates/')

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        choices=[(i, f"{i} звёзд") for i in range(1, 6)],
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'user')

    def __str__(self):
        return f"{self.user.username} → {self.course.course_name} ({self.rating})"
