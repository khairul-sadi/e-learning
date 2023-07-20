from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Course, CourseContent
from .forms import RegistrationForm, LoginForm, CourseForm, CourseContentForm

# Create your views here.


def home(request):
    courses = Course.objects.all()
    context = {
        "courses": courses
    }
    return render(request, "devedu/home.html", context)


def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect("/login")
    else:
        form = RegistrationForm()

    context = {
        "form": form
    }
    return render(request, "registration/sign_up.html", context)


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        user_name = request.POST.get("username")
        password1 = request.POST.get("password1")

        user = authenticate(username=user_name, password=password1)
        if user:
            login(request, user)
            # if user.is_staff:  # type: ignore
            #     return redirect("admin_dashboard")
            return redirect("home")
    else:
        form = LoginForm()

    context = {
        "form": form
    }
    return render(request, "registration/login.html", context)


def admin_dashboard(request):
    courses = Course.objects.all()
    context = {
        "courses": courses
    }
    return render(request, "admin/dashboard.html", context)


#! Add Starts
# ? Check permissions before deleting
def add_new_course(request):
    if request.method == "POST":
        course = CourseForm(request.POST, request.FILES)

        if course.is_valid():
            course.save()
            id = Course.objects.get(title=request.POST.get("title"))
            return add_contents(request, id.id)  # type: ignore
    else:
        course = CourseForm()

    context = {
        "course": course
    }
    return render(request, "admin/add_course.html", context)

# ? Check permissions before deleting


def add_contents(request, id):
    course = Course.objects.get(pk=id)

    if request.method == "POST":
        content_form = CourseContentForm(request.POST, request.FILES)

        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.course = course
            content.save()

        return HttpResponseRedirect(reverse("add_content", args=[id]))

    context = {
        "course": course,
        "contents": course.contents.all(),  # type: ignore
        "content_form": CourseContentForm()
    }

    return render(request, "admin/add_contents.html", context)

# ! Add Ends


# ! Edits start
# ? Check permissions before deleting
def edit_course(request, id):
    course = Course.objects.get(pk=id)
    course_form = CourseForm(instance=course)
    # ! all() gives multiple contents so it wouldn't work like that
    contents = course.contents.all()  # type: ignore
    # content_form = CourseContentForm(instance=content)

    if request.method == "POST":
        course_form = CourseForm(request.POST, request.FILES, instance=course)
        if course_form.is_valid():
            course_form.save()
            return HttpResponseRedirect(reverse("edit_course", args=[id]))

    context = {
        "course": course,
        "course_form": course_form,
        "contents": contents,
        # "content_form": content_form
    }

    return render(request, "admin/edit_course.html", context)


# ? Check permissions before deleting
def edit_content(request, id):
    content = CourseContent.objects.get(pk=id)
    content_form = CourseContentForm(instance=content)
    course = Course.objects.get(contents=content)

    if request.method == "POST":
        content_form = CourseContentForm(
            request.POST, request.FILES, instance=content)
        if content_form.is_valid():
            content_form.save()
            # HttpResponseRedirect(reverse("edit_content", args=[id]))

            return redirect(
                reverse("edit_course", args=[course.id])  # type: ignore
            )
    context = {
        "course": course,
        "content": content,
        "content_form": content_form
    }
    return render(request, "admin/edit_content.html", context)

# ! Edits Ends


# ! DELETE STARTS
# ? Check permissions before deleting
def delete_course(request, id):
    course = Course.objects.get(pk=id)

    if request.method == "POST":
        course.delete()
        return redirect("admin_dashboard")

    context = {
        "course": course
    }

    return render(request, "admin/delete_course.html", context)


# ? Check permissions before deleting
def delete_content(request, id):
    content = CourseContent.objects.get(pk=id)
    course = Course.objects.get(contents=content)

    if request.method == "POST":
        content.delete()
        return redirect(
            reverse("edit_course", args=[course.id])  # type:ignore
        )

    context = {
        "content": content
    }
    return render(request, "admin/delete_content.html", context)

# ! DELETE ENDS
