from django import forms
from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth.models import User

from .models import Course, CourseContent


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


class CourseContentForm(forms.ModelForm):
    class Meta:
        model = CourseContent
        exclude = ["course"]
        # fields = ['serial', "title", 'file']


# CourseFormSet = forms.inlineformset_factory(
#     Course, CourseContent, form=CourseContentForm, extra=1)
