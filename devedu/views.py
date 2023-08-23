from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from django.urls import reverse

from django.contrib.auth.models import User

from django.db.models import Q

from .models import Course, CourseContent, UserProfile, Instructor, Review, ReviewCourseMiddle, Tag
from .forms import RegistrationForm, LoginForm, CourseForm, CourseContentForm, UserProfileForm, ReviewForm

# Create your views here.


def home(request):
    courses = Course.objects.all().order_by("-avg_rating")[:8]
    reviews = Review.objects.all().order_by("-rating")[:3]
    context = {
        "courses": courses,
        "reviews": reviews,
    }
    return render(request, "devedu/home.html", context)


@login_required(login_url="/login")
def enroll_course(request, slug, username):
    user = User.objects.get(username=username)
    if user.is_staff:
        message = "This user is a staff. Try a Student account to enroll."
        # ! redirect to the course detail page
        return redirect(reverse("course_detail", args=[slug]))
    user_profile = UserProfile.objects.get(user=user)
    course = Course.objects.get(slug=slug)
    instractor = course.author
    enrolled = course.enrolled_students.all()
    if user_profile == instractor.user:  # type: ignore
        message = "You are the Instractor of this course!"
        # ! redirect to the course detail page
        # return redirect("course_detail")
        return redirect(reverse("course_detail", args=[course.slug]))
    if user_profile in enrolled:
        message = "You're already enrolled in this course!"
        # ! redirect to the course detail page
        # return redirect("course_detail")
        return redirect(reverse("course_detail", args=[course.slug]))
    else:
        response = course.enrolled_students.add(user_profile)
        if response:
            message = "Course added successfully."
        else:
            message = "Course didn't added successfully. Try again later."
    context = {
        "message": message,
        "course": course,
        "en_students": enrolled,
    }
    return redirect(reverse("course_detail", args=[course.slug]))

# !------------------------ LOG SIGN starts ----------------------------#


def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            # ? following line is edited
            UserProfile.objects.create(user=user)
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
            return redirect("home")
    else:
        form = LoginForm()

    context = {
        "form": form
    }
    return render(request, "registration/login.html", context)

# !------------------------ LOG SIGN end ----------------------------#


# ! -----------------------------USER PROFILE AND EDIT PROFILE START---------------#
def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        user = None
        # ! Gives error otherwist
        return render(request, "devedu/home.html", {})
    user_profile = UserProfile.objects.get(user=user)
    enrolled_courses = user_profile.courses.all()  # type: ignore
    context = {
        "en_courses": enrolled_courses,
        "user_profile": user_profile
    }
    return render(request, "devedu/user_profile.html", context)


# ? Check if the same user is trying to edit or not
def edit_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        user = None
        # ! Gives error otherwist
        return render(request, "devedu/home.html", {})
    user_profile = UserProfile.objects.get(user=user)
    user_profile_form = UserProfileForm(instance=user_profile)
    if request.method == "POST":
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return HttpResponseRedirect(reverse("user_profile", args=[username]))

    context = {
        "user_profile": user_profile,
        "user_profile_form": user_profile_form
    }
    return render(request, "devedu/edit_profile.html", context)

# ! -----------------------USER PROFILE AND EDIT PROFILE END-------------------------#


# ! ----------------------------COURSE DETAIL starts-----------------#

def course_detail(request, slug):
    course = Course.objects.get(slug=slug)
    contents = course.contents.all().order_by("serial")  # type: ignore
    reviews = course.reviews.all().order_by("-review__rating")  # type: ignore
    try:
        free_content = contents.filter(is_free=True)[0]
    except:
        free_content = ""
    enrolled_students = course.enrolled_students.all()

    reviewers = []
    for r in reviews:
        reviewers.append(r.review.author.user)

    en_students = []
    for stu in enrolled_students:
        en_students.append(stu.user)
    context = {
        "course": course,
        "contents": contents,
        "reviews": reviews,
        "tot_reviews": len(reviewers),
        "free_content": free_content,
        "en_students": en_students,
    }
    return render(request, "devedu/course_detail.html", context)


def all_courses(request):
    courses = Course.objects.all()
    context = {
        "courses": courses,
    }
    return render(request, "devedu/all_courses.html", context)


def learning(request, username, slug):
    course = Course.objects.get(slug=slug)
    contents = course.contents.all().order_by("serial")  # type: ignore
    free_content = contents.filter(is_free=True)[0]
    context = {
        "course": course,
        "contents": contents,
        "free_content": free_content
    }
    return render(request, "devedu/learning.html", context)


# ! ------------------------------COURSE DETAIL ends---------------------#


# ! ------------------------------ Search Start ---------------------#
def search(request):
    query = request.GET.get("q")
    if query:
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__user__first_name__icontains=query) |
            Q(author__user__last_name__icontains=query)).order_by("-avg_rating")
    else:
        courses = Course.objects.all().order_by("-avg_rating")

    context = {
        "courses": courses,
        "query": query,
    }
    return render(request, "devedu/all_courses.html", context)


def filter(request):
    query = request.GET.get("query")
    filter = request.GET.get("filter")
    sort = request.GET.get("sort")

    if query == "all-courses":
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__user__first_name__icontains=query) |
            Q(author__user__last_name__icontains=query))

    if filter != "all-courses":
        tag = Tag.objects.filter(caption=filter)
        courses = courses.filter(tags__in=tag)

    courses = courses.order_by(sort)
    serialized_courses = serialize("json", courses)

    context = {
        "courses": serialized_courses,
        "query": query,
    }

    return JsonResponse(context)


def get_author(request):
    author = Instructor.objects.get(pk=request.GET.get("id")).user
    username = author.user.username
    first_name = author.first_name
    last_name = author.last_name

    context = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
    }
    return JsonResponse(context)

# ! ------------------------------ Search ends---------------------#


# ! ------------------------------ REVIEW STARTS ---------------------#
def review(request, slug, username):
    user = User.objects.get(username=username)
    userProfile = UserProfile.objects.get(user=user)
    review_form = ReviewForm()
    course = Course.objects.get(slug=slug)
    reviews = course.reviews.all().order_by("-review__rating")  # type: ignore

    reviewers = []
    for r in reviews:
        reviewers.append(r.review.author.user)

    enrolled_students = course.enrolled_students.all()
    en_students = []
    for stu in enrolled_students:
        en_students.append(stu.user)

    if request.method == "POST":
        if user in en_students and not user in reviewers:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.author = userProfile
                review.save()
                reviewMid = ReviewCourseMiddle.objects.create(
                    course=course, review=review)
                all_reviews = course.reviews.all()  # type:ignore
                tot_rating = 0
                for r in all_reviews:
                    tot_rating += r.review.rating
                course.avg_rating = tot_rating / len(all_reviews)
                course.save()
                return redirect(reverse("review", args=[slug, username]))
        else:
            return redirect("home")

    context = {
        "course": course,
        "reviews": reviews,
        "review_form": review_form,
        "reviewers": reviewers,
        "tot_reviews": len(reviewers),
        # "avg_rating": avg_rating,
    }
    return render(request, "devedu/review.html", context)

# ! ------------------------------ REVIEW ENDS -----------------------#


# ! --------------------------------Application-------------------------------#
@login_required(login_url="/login")
def apply(request, username):
    user = User.objects.get(username=username)
    user_form = UserProfileForm()

    if not user.is_staff:
        user_profile = UserProfile.objects.get(user=user)
        if request.method == "POST":
            user_form = UserProfileForm(
                request.POST, request.FILES, instance=user_profile)
            if user_form.is_valid():
                user_profile.applied = True
                user_profile.save()
                user_form.save()
                return redirect("home")
        else:
            user_form = UserProfileForm(instance=user_profile)
    else:
        user_profile = False
    context = {
        "user_profile": user_profile,
        "user_form": user_form,
    }
    return render(request, "devedu/apply.html", context)
# ! ------------------------------Application Ends----------------------------#


# ? ALL ADMIN PANEL BELOW START
def admin_dashboard(request):
    courses = Course.objects.all()
    context = {
        "courses": courses
    }
    return render(request, "admin/dashboard.html", context)


#! --------------------------------- Add Starts ------------------------------------#
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

# ! -------------------------------- Add Ends -------------------------------#


# ! -------------------------------- Edits start ------------------------------#
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


# !----------------------- DELETE STARTS----------------------------#
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

# ! -------------------------------DELETE ENDS------------------------------------------#


# !----------------------------- Applications start ----------------------------#
def admin_applications(request):
    users = UserProfile.objects.filter(applied=True)
    context = {
        "users": users,
    }
    return render(request, "admin/applications.html", context)


def accept(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    user_profile.is_instructor = True
    user_profile.applied = False
    user_profile.save()
    Instructor.objects.create(user=user_profile)
    return redirect("admin_applications")


def reject(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    user_profile.is_instructor = False
    user_profile.applied = False
    user_profile.save()
    return redirect("admin_applications")

# !----------------------------- Applications end ----------------------------#
# ? -----------------------------Admin panel ends---------------------------------------#
