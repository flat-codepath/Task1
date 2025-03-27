from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
      path('register/',views.UserRegisterationApiView.as_view(),name='register'),
      path('',views.UserLoginView.as_view(),name='login'),
      path("profile/<int:pk>",views.ProfileView.as_view(),name='profile'),

      path("student_profile/<int:pk>",views.getStudentProfileView.as_view(),name='student_profile'),
      path('student_list/',views.ListStudentProfileView.as_view(),name='student_list'),
      path('edit_student/<int:pk>',views.StudentProfileEditView.as_view(),name='edit_student'),

      path('teacher_profile/<int:pk>',views.getTeacherProfileView.as_view(),name='get_student'),
      path('teacher_list/',views.ListTeacherProfileView.as_view(),name='teacher_list'),
      path('edit_teacher/<int:pk>',views.EditTeacherProfileView.as_view(),name='edit_teacher')
      
]



