from django import forms
from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth.models import User

from .models import Course, CourseContent, UserProfile, Review


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1"]


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        exclude = ["slug", "enrolled_students", "avg_rating",
                   "quiz", "git_repository", "discord"]


class CourseContentForm(forms.ModelForm):
    class Meta:
        model = CourseContent
        exclude = ["course"]
        # fields = ['serial', "title", 'file']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["user", "is_instructor", "applied"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["author"]
