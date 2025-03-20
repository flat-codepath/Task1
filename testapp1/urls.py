from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
      path('register/',views.UserRegisterationApiView.as_view(),name='register'),
      path('login/',views.UserLoginView.as_view(),name='login')
]



