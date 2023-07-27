from django.contrib import admin

from .models import Course, CourseContent, UserProfile, Instructor

# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = ["author", "title"]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseContent)
admin.site.register(UserProfile)
admin.site.register(Instructor)
