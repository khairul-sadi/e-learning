from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    title = models.CharField(unique=True, max_length=150, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField(validators=[MaxLengthValidator(500)])
    thumb_nail = models.ImageField(upload_to="thumb_nails", null=True)
    created_on = models.DateField(auto_now=True)
    last_updated_on = models.DateField(auto_now=True)
    price = models.FloatField()

    def __str__(self):
        return f"{self.title} {self.author}"


class CourseContent(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, related_name="contents")
    serial = models.IntegerField(null=True)
    title = models.CharField(max_length=150, null=True)
    file = models.FileField(null=True)
