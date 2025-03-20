from django import forms
from django.contrib.auth.forms import UserCreationForm


from . models import User,Admin,Teacher,Student

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'role', 'sub_organization','password1', 'password2']



class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['name', 'date_of_birth', 'date_of_joining', 'phone_number', 'address']


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model =Teacher
        fields=['name','date_of_birth','date_of_joining','phone_number', 'address','subjects', 'salary']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model =Student
        fields=['name','date_of_birth','date_of_joining','phone_number', 'address','roll_number','student_class','student_section']




