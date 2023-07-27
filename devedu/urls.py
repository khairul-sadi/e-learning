from django.urls import path

from . import views
# , admin_dashboard, signup, log_in, profile, add_course

# ? Note: Static URLs have to be in the top then dynamic URLs

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.user_login, name="login"),
    path("sign-up", views.signup, name="sign_up"),
    # ! Admin
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
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
    # ! course detail
    # ? use course slug
    path("course-detail/<slug:slug>", views.course_detail, name="course_detail")
]
