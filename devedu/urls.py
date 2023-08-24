from django.urls import path

from . import views
# , admin_dashboard, signup, log_in, profile, add_course

# ? Note: Static URLs have to be in the top then dynamic URLs

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.user_login, name="login"),
    path("sign-up", views.signup, name="sign_up"),
    # ! Admin
    path("admin-dashboard/courses", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/applications",
         views.admin_applications, name="admin_applications"),
    path("filter/", views.filter, name="filter"),
    path("get-author/", views.get_author, name="get_author"),
    path("all-courses", views.all_courses, name="all_courses"),
    path("search", views.search, name="search"),

    path("admin-dashboard/applications/<str:username>",
         views.accept, name="accept_application"),
    path("admin-dashboard/applications/<str:username>",
         views.reject, name="reject_application"),
    path("admin-dashboard/add-course",
         views.add_new_course, name="add_new_course"),
    path("admin-dashboard/add-course/add-content/<int:id>",
         views.add_contents, name="add_content"),
    path("admin-dashboard/edit-course/<int:id>",
         views.edit_course, name="edit_course"),
    path("admin-dashboard/delete-course/<int:id>",
         views.delete_course, name="delete_course"),
    path("admin-dashboard/edit-content/<int:id>",
         views.edit_content, name="edit_content"),
    path("admin-dashboard/delete-content/<int:id>",
         views.delete_content, name="delete_content"),
    # ! user
    path("<str:username>", views.user_profile, name="user_profile"),
    path("edit-profile/<str:username>", views.edit_profile, name="edit_profile"),
    path("apply/<str:username>", views.apply, name="apply"),
    # ! course detail
    # ? use course slug
    path("course-detail/<slug:slug>", views.course_detail, name="course_detail"),

    path("payment/<slug:slug>/<str:username>", views.payment, name="payment"),
    path("payment/<slug:slug>/<str:username>/<str:customer_id>",
         views.success, name="pay_success"),
    path("payment/<str:message>",
         views.payment_error, name="payment_error"),

    path("course-detail/<slug:slug>/<str:username>/<str:customer_id>",
         views.enroll_course, name="enroll_course"),
    path("course/<slug:slug>/<str:username>", views.review, name="review"),
    path("my-learnings/<str:username>/<slug:slug>",
         views.learning, name="learning"),
]
