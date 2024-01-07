from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('registerpage', views.registerpage, name ='registerpage'),

    path('register_user', views.register_user, name='register_user'),

    path('loginpage', views.loginpage, name='loginpage'),

    path('login_user', views.login_user, name='login_user'),

    path('userprofile', views.userprofile, name='userprofile'),

    path('updateprofile', views.updateprofile, name='updateprofile'),

    path('update_user', views.update_user, name='update_user'),

    path('logout_user', views.logout_user, name='logout_user'),

    path('adminprofile', views.adminprofile, name='adminprofile'),

    path('add_course_page', views.add_course_page, name='add_course_page'),

    path('add_course', views.add_course, name='add_course'),

    path('add_student_page', views.add_student_page, name='add_student_page'), 

    path('add_student', views.add_student, name='add_student'),    

    path('view_student_page', views.view_student_page, name='view_student_page'), 

    path('student_update_page/<int:student_id>/', views.student_update_page, name='student_update_page'),

    path('student_update/<int:student_id>/', views.student_update, name='student_update'),   

    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),

    path('view_teacher_page', views.view_teacher_page, name='view_teacher_page'),  

    path('delete_teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),

    path('logout_admin', views.logout_admin, name='logout_admin'),      
]
