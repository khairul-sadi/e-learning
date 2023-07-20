from django.contrib import admin

from .models import Course, CourseContent

# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = ["author", "title"]


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseContent)
