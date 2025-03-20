from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.

class Organization(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

 
class SubOrganization(models.Model):
    name=models.CharField(max_length=100)
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='sub_organizations')
    class Meta:
        unique_together=('name','organization')


    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES=(
        ("admin","Admin"),
        ("teacher",'Teacher'),
        ("student","Student")
    )
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,null=True,blank=True)
    sub_organization=models.ForeignKey(SubOrganization,on_delete=models.SET_NULL,null=True,blank=True,related_name='users')
    
    
    def __str__(self):
        return f'{self.username}-{self.role}'
    
    

class Subject(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

class Class(models.Model):
    name=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class Section(models.Model):
    name= models.CharField(max_length=100)
    student_class=models.ForeignKey(Class,on_delete=models.CASCADE,related_name='sections')
    
    class Meta:
        unique_together = ('name', 'student_class')
    
    def __str__(self):
        
        return  f'{self.student_class.name} - {self.name} '
    

    



# Abstract Profile Model
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    date_of_birth=models.DateField()
    date_of_joining=models.DateField()
    phone_number=models.CharField(max_length=10, validators=[RegexValidator(r'^[789]\d{9}$', 'Enter a valid 10-digit phone number')])
    address=models.TextField(null=True)

    class Meta:
        abstract = True
        
    def __str__(self):
        return self.name
    
    
class Admin(Profile):
    def save(self, *args, **kwargs):
        if self.user.role != 'admin':
            pass
        else:
             super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Teacher(Profile):
    # teacher_class=models.OneToOneField(Class,on_delete=models.SET_NULL,blank=True,null=True,related_name='class_teacher')
    subjects=models.ManyToManyField(Subject,related_name='teachers')
    salary=models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.name



class Student(Profile):
    roll_number=models.CharField(max_length=15,unique=True)
    student_class=models.ForeignKey(Class,on_delete=models.CASCADE)
    student_section=models.ForeignKey(Section,on_delete=models.SET_NULL,blank=True,null=True)

    def save(self, *args, **kwargs):
        if self.user.role != 'student':
            pass
        else:
            super().save(*args, **kwargs)

    def __str__(self):
       return f"{self.name} - {self.student_class}"

